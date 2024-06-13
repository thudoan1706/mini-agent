import asyncio
import re
import networkx as nx
from collections import defaultdict
from typing import Dict, Tuple

from llama_index.core.tools import AsyncBaseTool, ToolOutput
from llama_index.core.types import BaseOutputParser
from llama_index.packs.agents_coa.output_parser import ChainOfAbstractionParser

from llama_index.core.tools import AsyncBaseTool, ToolOutput
from llama_index.core.types import BaseOutputParser
from llama_index.packs.agents_coa.output_parser import ChainOfAbstractionParser


class CustomChainOfAbstractionParser(ChainOfAbstractionParser):
    def __init__(self, verbose: bool = False):
        super().__init__(verbose)

    async def aparse(
        self, solution: str, tools_by_name: Dict[str, AsyncBaseTool]
    ) -> Tuple[str, int]:
        # Extract function calls and placeholders
        func_calls = re.findall(r"\[FUNC (\w+)\((.*?)\) = (\w+)\]", solution)
        print("This is func_calls", func_calls)

        placeholders = set()
        for match in re.finditer(r"\[FUNC (\w+)\((.*?)\) = (\w+)\]", solution):
            placeholders.add(match.group(3))

        # Create a dependency graph
        graph = nx.DiGraph()
        for func_name, inputs, output in func_calls:
            print("This is the function name:", func_name)
            try:
                # Minimal modification to split inputs manually
                inputs_list = [inp.strip() for inp in inputs.split(',')]
                print("Parsed inputs:", inputs_list)
            except Exception as e:
                print(f"Error while parsing inputs: {e}")
                raise
            print(func_name, inputs_list, output)

            if output in inputs_list:
                print(
                    f"Skipping self-dependency in {func_name}({inputs_list}) = {output}")
                continue

            graph.add_node(output, func_name=func_name, inputs=inputs_list)
            for inp in inputs_list:
                graph.add_edge(inp, output)

        print("Graph nodes:", graph.nodes(data=True))
        print("Graph edges:", graph.edges())

        # Find the execution levels
        execution_levels = defaultdict(list)
        for node in nx.topological_sort(graph):
            level = (
                max(
                    [execution_levels[pred]
                        for pred in graph.predecessors(node)],
                    default=-1,
                )
                + 1
            )
            execution_levels[node] = level

        # Group nodes by execution level
        level_groups = defaultdict(list)
        for node, level in execution_levels.items():
            level_groups[level].append(node)

        # Execute functions and replace placeholders
        results = {}
        tool_outputs = []
        graph_nodes = {node[0]: node[1] for node in graph.nodes(data=True)}
        for level in sorted(level_groups.keys()):
            level_nodes = level_groups[level]
            parallel_results = {}
            for placeholder in level_nodes:
                if len(graph_nodes[placeholder]) == 0:
                    continue

                # get function name and inputs
                func_name, inputs = (
                    graph_nodes[placeholder]["func_name"],
                    graph_nodes[placeholder]["inputs"],
                )

                # loop up any inputs that depend on other functions
                input_values = [results.get(inp, inp) for inp in inputs]
                if self._verbose:
                    print(
                        f"==== Executing {func_name} with inputs {input_values} ====",
                        flush=True,
                    )

                # execute function and store result
                try:
                    raw_tool_output = await tools_by_name[func_name].acall(
                        *input_values
                    )
                    tool_outputs.append(
                        ToolOutput(
                            content=str(raw_tool_output),
                            tool_name=func_name,
                            raw_output=raw_tool_output,
                            raw_input={"args": input_values},
                            is_error=False,
                        )
                    )
                except Exception as e:
                    tool_outputs.append(
                        ToolOutput(
                            content=str(e),
                            tool_name=func_name,
                            raw_output=None,
                            raw_input={"args": input_values},
                            is_error=True,
                        )
                    )

                    # If an error occurs, stop execution
                    break

                parallel_results[placeholder] = str(raw_tool_output)
            results.update(parallel_results)

        # Replace placeholders in the solution text
        for placeholder, value in results.items():
            solution = solution.replace(
                f"{placeholder}", '"' + str(value) + '"')

        return solution, tool_outputs

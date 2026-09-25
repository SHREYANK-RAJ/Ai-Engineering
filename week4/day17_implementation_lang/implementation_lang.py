# ============================================================
# LANGGRAPH IMPLEMENTATION
# Problem:
# Keep doubling a number until it becomes >= 100.
# Then print the final number and end the graph.
# ============================================================


# TypedDict is used to define the structure of our State.
from typing import TypedDict

# StateGraph is used to create the graph.
# END represents the end of the LangGraph execution.
from langgraph.graph import END, StateGraph


# ============================================================
# 1. STATE
# ============================================================
# State is like a shared whiteboard.
# All nodes can read the data stored inside it.
#
# Here our state contains only one piece of data:
# "number" -> an integer.
# ============================================================

class State(TypedDict):
    number: int


# ============================================================
# 2. NODE: DOUBLE
# ============================================================
# A node is a Python function that works directly on the State.
#
# This node:
# 1. Reads the current number from the state.
# 2. Doubles it.
# 3. Returns the updated number.
#
# IMPORTANT:
# A LangGraph node returns a dictionary containing
# the state values that it wants to update.
# ============================================================

def double(state: State) -> dict:

    # Read the current number from the shared state.
    boardnum = state["number"]

    # Double the current number.
    newnum = boardnum * 2

    # Show that the double node is running.
    print("in double")

    # Print the new number.
    print(newnum)

    # Return the updated state.
    # LangGraph will automatically update the State.
    return {"number": newnum}


# ============================================================
# 3. NODE: FINISH
# ============================================================
# This is another node.
#
# Its job is simply to:
# 1. Read the final number.
# 2. Print it.
# 3. Keep the same value in the state.
#
# It does not actually change the number.
# ============================================================

def finish(state: State) -> dict:

    # Read the current number from the shared state.
    boardnum = state["number"]

    # Show that the finish node is running.
    print("in finish")

    # Print the final number.
    print(boardnum)

    # Return the same number because the node
    # is not changing anything.
    return {"number": boardnum}


# ============================================================
# 4. DECISION / HELPER FUNCTION
# ============================================================
# This is NOT a node.
#
# Why?
# Because it does not modify the State.
# It only reads the State and decides which node
# should execute next.
#
# If number < 100:
#       go back to "double"
#
# Otherwise:
#       go to "finish"
# ============================================================

def decision(state: State) -> str:

    # Check the current number.
    if state["number"] < 100:

        # Continue doubling.
        return "double"

    else:

        # Number has reached/exceeded 100.
        return "finish"


# ============================================================
# 5. CREATE THE GRAPH
# ============================================================
# StateGraph(State) creates the graph using our State structure.
#
# "builder" is used to construct the graph.
# ============================================================

builder = StateGraph(State)


# ============================================================
# 6. ADD NODES
# ============================================================
# add_node("node_name", python_function)
#
# The first argument is the name LangGraph uses for the node.
# The second argument is the actual Python function.
# ============================================================

builder.add_node("double", double)

builder.add_node("finish", finish)


# ============================================================
# 7. SET ENTRY POINT
# ============================================================
# The entry point tells LangGraph:
#
# "When execution starts, begin from the double node."
# ============================================================

builder.set_entry_point("double")


# ============================================================
# 8. ADD CONDITIONAL EDGE
# ============================================================
# This creates the decision/loop.
#
# Starting node:
#       "double"
#
# Decision function:
#       decision
#
# Possible results:
#
#       decision() returns "double"
#               ↓
#       go back to the "double" node
#
#       decision() returns "finish"
#               ↓
#       go to the "finish" node
# ============================================================

builder.add_conditional_edges(
    "double",
    decision,
    {
        "double": "double",
        "finish": "finish",
    },
)


# ============================================================
# 9. CONNECT FINISH TO END
# ============================================================
# "finish" is our last node.
#
# END means:
#       Stop the LangGraph execution.
#
# So:
#
#       finish → END
# ============================================================

builder.add_edge("finish", END)


# ============================================================
# 10. COMPILE THE GRAPH
# ============================================================
# compile() converts the graph we created with the builder
# into an executable LangGraph application.
# ============================================================

graph = builder.compile()


# ============================================================
# 11. RUN THE GRAPH
# ============================================================
# This is the standard Python entry-point check.
#
# The code inside this block runs when this file is
# executed directly.
# ============================================================

if __name__ == "__main__":

    # graph.invoke() starts the LangGraph execution.
    #
    # Our State requires:
    #       number: int
    #
    # We start with number = 5.
    result = graph.invoke({"number": 5})

    # Print the final state returned by LangGraph.
    print("Final State:", result)


# ============================================================
# EXECUTION FLOW
# ============================================================
#
# Initial State:
#       {"number": 5}
#
#        ↓
#
#      double
#       5 × 2 = 10
#
#        ↓
#
#      decision
#       10 < 100
#       → "double"
#
#        ↓
#
#      double
#       10 × 2 = 20
#
#        ↓
#
#      decision
#       20 < 100
#       → "double"
#
#        ↓
#
#      double
#       20 × 2 = 40
#
#        ↓
#
#      decision
#       40 < 100
#       → "double"
#
#        ↓
#
#      double
#       40 × 2 = 80
#
#        ↓
#
#      decision
#       80 < 100
#       → "double"
#
#        ↓
#
#      double
#       80 × 2 = 160
#
#        ↓
#
#      decision
#       160 < 100  → FALSE
#       → "finish"
#
#        ↓
#
#      finish
#       prints 160
#
#        ↓
#
#       END
#
#
# ============================================================
# MAIN LANGGRAPH CONCEPTS IN THIS CODE
# ============================================================
#
# STATE
# -----
# class State(TypedDict):
#     number: int
#
# State is the shared data/whiteboard.
#
#
# NODE
# ----
# double()
# finish()
#
# Nodes are Python functions that work directly with State
# and return a dictionary containing state updates.
#
#
# HELPER / DECISION FUNCTION
# --------------------------
# decision()
#
# This reads the State and decides where the graph should go.
# It does not modify the State, so it is not a node.
#
#
# EDGE
# ----
# An edge tells LangGraph what should execute after a node.
#
# Here we use a CONDITIONAL EDGE:
#
# double
#    |
#    ↓
# decision
#   / \
#  /   \
# ↓     ↓
# double finish
#
#
# END
# ---
# finish → END
#
# END tells LangGraph that execution is complete.
#
#
# COMPILE
# -------
# graph = builder.compile()
#
# Converts the graph definition into an executable graph.
#
#
# INVOKE
# ------
# graph.invoke({"number": 5})
#
# Starts the graph with the initial State.
#
# ============================================================
# FINAL FLOW
# ============================================================
#
# State → Nodes → Decision → Conditional Edge
#                         ↓
#                 ┌───────┴────────┐
#                 ↓                ↓
#               double           finish
#                 ↓                ↓
#               repeat            END
#
# ============================================================
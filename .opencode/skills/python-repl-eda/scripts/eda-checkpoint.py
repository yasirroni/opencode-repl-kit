# Pickle Checkpoint Template

"""
Save and load REPL state for recovery after session restart.

Usage in REPL:
    exec(open('temp/eda_checkpoint.py').read())
    checkpoint_save(data=ds, nodes=nodes_df, edges=edges_df)

    # After session restart:
    exec(open('temp/eda_checkpoint.py').read())
    state = checkpoint_load()
    ds = state['data']
    nodes_df = state['nodes']
    edges_df = state['edges']
"""

import pickle

def checkpoint_save(**kwargs):
    """Save variables to temp/checkpoint.pkl."""
    with open('temp/checkpoint.pkl', 'wb') as f:
        pickle.dump(kwargs, f)
    print(f"Checkpoint saved: {list(kwargs.keys())}")

def checkpoint_load():
    """Load variables from temp/checkpoint.pkl."""
    with open('temp/checkpoint.pkl', 'rb') as f:
        return pickle.load(f)

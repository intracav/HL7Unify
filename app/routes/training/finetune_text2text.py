"""
    This route will be used to fine tune a text2text transformer model to standardize HL7 messages.
    
    Using huggingface datasets, we can load the HL7 dataset and fine tune a text2text transformer model to standardize HL7 messages.
"""

from datasets import load_dataset


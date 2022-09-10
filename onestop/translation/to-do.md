pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_trf

Tips for efficient processing (https://spacy.io/usage/processing-pipelines)
Process the texts as a stream using nlp.pipe and buffer them in batches, instead of one-by-one. 
This is usually much more efficient. Only apply the pipeline components you need. 
Getting predictions from the model that you don’t actually need adds up and becomes very inefficient at scale. 
To prevent this, use the disable keyword argument to disable components you don’t 
need – either when loading a pipeline, or during processing with nlp.pipe. 
See the section on disabling pipeline components for more details and examples.

Use senter rather than parser for fast sentence segmentation
If you need fast sentence segmentation without dependency parses, disable the parser use the senter component instead:


# Debias

## Install
```bash
# https://github.com/oyzh888/debias
git clone git@github.com:oyzh888/debias.git
cd ./debias
sh install.sh
```

## Metric
```bash
# If you want to do a new test, please delete the res in the data/openai_res, otherwise the code will read the cache :)
python debias/metric/gpt.py
python debias/metric/parse_gpt_res.py
```

Example output:
```bash
{
  "Accuracy": 1.0,
  "Keywords Matching": 1.0,
  "Music Metrics": {
    "Human Likability": 0.9,
    "Creativity": 0.8,
    "Relevance": 1.0,
    "Coherence": 1.0,
    "Emotional Resonance": 0.9,
    "Cultural Appropriateness": 0.8
  },
  "Reason": "Perfect match to groundtruth"
}
4.443441152572632
{
  "Accuracy": 0.85,
  "Keywords Matching": 0.9,
  "Music Metrics": {
    "Human Likability": 0.8,
    "Creativity": 0.7,
    "Relevance": 0.9,
    "Coherence": 0.9,
    "Emotional Resonance": 0.9,
    "Cultural Appropriateness": 0.6
  },
  "Reason": "Mismatched genre, but similar themes"
}
8.301937341690063
Results exported to /Users/ouyangzhihao/Desktop/code_bd/debias/data/export_metric.csv
Average Accuracy: 0.93
Average Keywords Matching: 0.95
Average Music Metrics:
  Human Likability: 0.85
  Creativity: 0.75
  Relevance: 0.95
  Coherence: 0.95
  Emotional Resonance: 0.90
  Cultural Appropriateness: 0.70
```
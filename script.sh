#MAllet command to generate 10 topics
bin/mallet train-topics --input csss.mall --num-topics 10 --output-state csss-state.gz --output-topic-keys csss_keys.txt --output-doc-topics people.txt --optimize-interval 20

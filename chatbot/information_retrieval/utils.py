def tokenize_sentences(tokenizer, text):
    sentences = tokenizer.tokenize_sentences(text)
    final_sentences = []

    for sentence in sentences:
        last_index = -1
        should_add_sentence = True
        for i in range(len(sentence)):
            if sentence[i] == '\n':
                if last_index == -1:
                    last_index = i
                elif i - last_index == 1:
                    last_index = i
                else:
                    should_add_sentence = False

        if should_add_sentence:
            final_sentences.append(sentence)

    return [
        tokenizer.tokenize_words(sentence)
        for sentence in final_sentences
        ]
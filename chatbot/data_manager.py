class DataManager():
    ANSWER_FULL_FORMAT = '{subject} {verb} {related_nodes}.'
    ANSWER_NO_RELATIONS_FORMAT = 'I know {subject}, but I don\'t know what {subject} {verb}.'

    def __init__(self, text_processor, db_service, wiki_service, parser, svo_extractor, summarizer):
        self.text_processor = text_processor
        self.db_service = db_service
        self.wiki_service = wiki_service
        self.parser = parser
        self.svo_extractor = svo_extractor
        self.summarizer = summarizer
        self.parsed_tree = None
        self.svos = None

    def parse_input(self, tokenized_sentence):
        self.tree = self.parser.parse(tokenized_sentence)
        self.svos = self.svo_extractor.get_svos(self.tree)

    def try_remember(self, tokenized_sentence):
        remembered = False

        for svo in self.svos:
            if self.svo_extractor.is_full_svo(svo):
                relation = self.text_processor.lemmatize(svo['verb'], 'v')

                subject = self.db_service.add(
                    name=svo['subject'].lower(),
                    original_name=svo['subject'])

                object = self.db_service.add(
                    name=svo['object'].lower(),
                    original_name=svo['object'])

                self.db_service.add_relation(subject, object, relation.lower())

                remembered = True

        return remembered

    def answer_from_database(self, tokenized_sentence):
        answer = None

        for svo in self.svos:
            if self.svo_extractor.is_full_sv(svo):
                self.text_processor.get_lemmas(svo['verb'], 'VERB')
                node = self.db_service.get(svo['subject'].lower())
                if node:
                    related_nodes = self.db_service.get_relations(node, svo['verb'].lower())
                    if related_nodes:
                        answer = self.ANSWER_FULL_FORMAT.format(
                            subject = svo['subject'],
                            verb = svo['verb'].lower(),
                            related_nodes = ', '.join(related_nodes)
                        )
                    else:
                        answer = self.ANSWER_NO_RELATIONS_FORMAT.format(
                            subject = svo['subject'],
                            verb = svo['verb']
                        )

        if answer and len(answer) > 1:
            answer = answer.capitalize()

        print('Answer from database: ', answer, '-'*30)

        return answer

    def get_search_phrases(self, tokenized_sentence):
        nj_phrases = self.svo_extractor.get_nj_phrases(self.tree)
        search_phrases = self.svo_extractor.get_search_phrases(nj_phrases)

        return search_phrases, nj_phrases

    def get_articles_from_wiki(self, search_phrases, only_intro = False, pages_for_phrase = 1):
        page_titles = set()
        for search_phrase in search_phrases:
            titles = self.wiki_service.search(search_phrase)[:pages_for_phrase]
            page_titles.update(titles)

        articles = []
        for title in page_titles:
            print('Getting page text for title : ', title)
            page_text = self.wiki_service.get(title, only_intro)
            article = {
                'title': title,
                'text': page_text
            }

            articles.append(article)
            print('Get finished: ', title)

        return articles

    def answer_from_wiki(self, search_phrases, titles_per_phrase, only_intro = False, nj_phrases = None):
        sentences = []
        articles = self.get_articles_from_wiki(search_phrases, only_intro, titles_per_phrase)
        if not articles:
            return None

        if nj_phrases:
            print('Summarizing by input frequency. This may take some time...')
            sentences = self.summarizer.summarize_by_input_frequency(3, articles, nj_phrases)
        else:
            print('Summarizing by word frequency in text. This may take some time...')
            sentences = self.summarizer.summarize_by_content_frequency(3, articles)

        print('Summarization finished...')

        summary = ' '.join(sentences)
        result = summary

        if len(articles) > 0 and len(summary) == 0:
            result = 'What do you mean? Be more specific.'

        return result



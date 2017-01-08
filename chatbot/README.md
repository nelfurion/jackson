# Jackson

## dialogue_manager.py

The dialogue manager will be responsible for all conversation actions. It is the one that knows when to read, answer, remember information. It basically will connect all the functionality.

## jackson.py

Setup for the actual chatbot.

## chatbot.py

Defines the chatbot class.

## config.py

Defines paths for models, etc.

## text_processor.py

Vectorization and tokenization of the input.

## question_types.py

Defines an enum for question types:
Declarative, Informative, nterrogative, Exclamatory.
They are used, by the dialogue manager to understand how to handle each input.

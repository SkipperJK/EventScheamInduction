from config import MODEL_DIR,USER_DICT_DIR
from pyltp import SentenceSplitter, Postagger, NamedEntityRecognizer, Parser



class LTPNLP:

    def __init__(self, user_dict_dir=MODEL_DIR, model_dir=USER_DICT_DIR):
        """

        :param user_dict_dir:
        :param model_dir:
        """



import pickle
from model.utils import Vocab
from transformers.tokenization_bert import BertTokenizer

# loading BertTokenizer
ptr_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased", do_lower_case=True)
idx_to_token = list(ptr_tokenizer.vocab.keys())
token_to_idx = {token: idx for idx, token in enumerate(idx_to_token)}
vocab = Vocab(
    idx_to_token,
    padding_token="[PAD]",
    unknown_token="[UNK]",
    bos_token=None,
    eos_token=None,
    reserved_tokens=["[CLS]", "[SEP]", "[MASK]"],
    token_to_idx=token_to_idx,
)

# save vocab
with open("pretrained/vocab.pkl", mode="wb") as io:
    pickle.dump(vocab, io)

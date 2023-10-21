from janome.analyzer import Analyzer
from janome.tokenfilter import ExtractAttributeFilter
from janome.tokenfilter import POSStopFilter
from janome.tokenfilter import POSKeepFilter
from janome.charfilter import RegexReplaceCharFilter, UnicodeNormalizeCharFilter
from janome.analyzer import Analyzer
from janome.tokenfilter import  TokenCountFilter
import numpy as np
from gensim import corpora,models
import chardet
import copy
from .models import Profile, Post, Comment,Dictionary

def get_string_from_file(filename):
    with open(filename, 'rb') as f:
        d = f.read()
        e = chardet.detect(d)['encoding']
        # 推定できなかったときはUTF-8で
        if e == None:
            e = 'UTF-8'
        return d.decode(e)
    
analyzer = Analyzer(
    char_filters=[
        UnicodeNormalizeCharFilter(),
        RegexReplaceCharFilter('[#!:;<>{}・`.,()-=$/_\d\'"\[\]\|]+', ' '),
    ],
    token_filters=[
        POSKeepFilter(['名詞']),
        # TokenCountFilter(sorted=True),
    ],
)

def get_words(string, keep_pos=None):
    
    
    analyzer = Analyzer(
        char_filters=[
            UnicodeNormalizeCharFilter(),
            RegexReplaceCharFilter('[#!:;<>{}・`.,()-=$/_\d\'"\[\]\|]+', ' '),
        ],
        token_filters=[
            POSKeepFilter(['名詞']),
            TokenCountFilter(sorted=True),
        ],
    )              # 後処理を指定
    words = []
    for word, count in analyzer.analyze(string):
      words.append(word) 


    return  words  #list(analyzer.analyze(string))

# def get_words(string, keep_pos=None):
#     filters = []
#     filters.append(RegexReplaceCharFilter('[#!:;<>{}・`.,()-=$/_\d\'"\[\]\|]+', ' '))
#     # RegexReplaceCharFilter('[#!:;<>{}・`.,()-=$/_\d\'"\[\]\|]+', ' ')
#     if keep_pos :
#         filters.append(POSKeepFilter(keep_pos))       # 指定品詞を抽出
#     filters.append(ExtractAttributeFilter('surface'))
    
#     a = Analyzer(token_filters=filters)               # 後処理を指定
#     return list(a.analyze(string))

def bows_to_cfs(bows):
    cfs = dict()
    for b in bows:
        for id, f in b:
            if not id in cfs:
                cfs[id] = 0
            cfs[id] += int(f)
    return cfs

def load_dictionary_and_corpus(dic_file, corpus_file):
    dic = corpora.Dictionary.load(dic_file)
    bows = list(corpora.MmCorpus(corpus_file))
    if not hasattr(dic, 'cfs'):
        dic.cfs = bows_to_cfs(bows)
    return dic, bows

def load_aozora_corpus():
    return load_dictionary_and_corpus('./media/aozora.dic','./media/aozora.mm')

# def load_aozora_corpus():
#     dic = np.load(
#     file="./media/save_dic.npy",        # npyかnpz拡張子のファイルを指定
#     allow_pickle=True,  )    # npy/npzで保存されたpickleファイルを読み込むかどうか (デフォルトではTrue)
#     bows = np.load(
#     file="./media/save_dic.npy",        # npyかnpz拡張子のファイルを指定
#     allow_pickle=True,      # npy/npzで保存されたpickleファイルを読み込むかどうか (デフォルトではTrue)
#     )
#     return dic,bows



def get_bows(texts, dic, allow_update=False):
    bows = []
    for text in texts:
        words = get_words(text, keep_pos=['名詞'])
        bow = dic.doc2bow(words, allow_update=allow_update)
        bows.append(bow)
    return bows



def add_to_corpus(texts, dic, bows, replicate=False):
    if replicate:
        dic = copy.copy(dic)
        bows = copy.copy(bows)
    texts_bows = get_bows(texts, dic, allow_update=True)
    bows.extend(texts_bows)
    return dic, bows, texts_bows

def get_weights(bows, dic, model, surface=False, N=1000):
    # TF・IDFを計算
    weights = model[bows]
    # TF・IDFの値を基準に降順にソート．最大でN個を抽出
    weights = [sorted(w,key=lambda x:x[1], reverse=True)[:N] for w in weights]
    if surface:
        return [[(dic[x[0]], x[1]) for x in w] for w in weights][0]
    else:
        return weights
    




def translate_bows(bows, table):
    return [[tuple([table[j[0]], j[1]]) for j in i if j[0] in table] for i in bows]
    

# def get_tfidfmodel_and_weights(text, pos=['名詞']):
#     dic, bows = load_aozora_corpus()
    
#     text_docs = get_words(text, keep_pos=pos) 
#     text_bows = dic.doc2bow(text_docs, allow_update=True)
#     bows.extend(text_bows)
    
#     # textsに現れる語のidとtoken(表層形)のリストを作成
#     text_ids = list(set([text_bows[i][j][0] for i in range(len(text_bows)) for j in range(len(text_bows[i]))]))
#     text_tokens = [dic[i] for i in text_ids]
    
#     # text_bowsにない語を削除．
#     dic.filter_tokens(good_ids=text_ids)
#     # 削除前後のIDの対応づけ
#     # Y = id2id[X] として古いid X から新しいid Y が得られるようになる
#     id2id = dict()
#     for i in range(len(text_ids)):
#         id2id[text_ids[i]] = dic.token2id[text_tokens[i]]
    
#     # 語のIDが振り直されたのにあわせてbowを変換
#     bows = translate_bows(bows, id2id)
#     text_bows = translate_bows(text_bows, id2id)
    
#     # TF・IDFモデルを作成
#     tfidf_model = models.TfidfModel(bows, normalize=True)
#     # モデルに基づいて重みを計算
#     text_weights = get_weights(text_bows, dic, tfidf_model)
    
#     return tfidf_model, dic, text_weights


def get_tfidfmodel_and_weights(texts, use_aozora=True, pos=['名詞']):
    if use_aozora:
        dic, bows = load_aozora_corpus()
    else:
        dic = corpora.Dictionary()
        bows = []
    
    text_docs = [get_words(text, keep_pos=pos) for text in texts]
    text_bows = [dic.doc2bow(d, allow_update=True) for d in text_docs]
    bows.extend(text_bows)
    
    # textsに現れる語のidとtoken(表層形)のリストを作成
    text_ids = list(set([text_bows[i][j][0] for i in range(len(text_bows)) for j in range(len(text_bows[i]))]))
    text_tokens = [dic[i] for i in text_ids]
    
    # text_bowsにない語を削除．
    dic.filter_tokens(good_ids=text_ids)
    # 削除前後のIDの対応づけ
    # Y = id2id[X] として古いid X から新しいid Y が得られるようになる
    id2id = dict()
    for i in range(len(text_ids)):
        id2id[text_ids[i]] = dic.token2id[text_tokens[i]]
    
    # 語のIDが振り直されたのにあわせてbowを変換
    bows = translate_bows(bows, id2id)
    text_bows = translate_bows(text_bows, id2id)
    
    # TF・IDFモデルを作成
    tfidf_model = models.TfidfModel(bows, normalize=True)
    # モデルに基づいて重みを計算
    text_weights = get_weights(text_bows, dic, tfidf_model)
    text_weights_token = get_weights(text_bows, dic, tfidf_model,surface=True)
    
    return tfidf_model, dic, text_weights,text_weights_token



# def jaccard(X, Y):
#     x = set(X)
#     y = set(Y)
#     a = len(x.intersection(y))
#     b = len(x.union(y))
#     if b == 0:
#         return 0
#     else:
#         return a/b
    
def getImportantWords(text,wordBoolean = True):
    text = [text]
    tfidf_model, dic, word_weight,text_weights_token = get_tfidfmodel_and_weights(text)
    if len(text_weights_token) < 4:
        text =  [r[0] for r in text_weights_token]
    elif wordBoolean :
        text = [r[0] for r in text_weights_token if r[1]>0.2 ]
    elif(len(text_weights_token) < 30):
        x = int(len(text_weights_token)*0.75)
        text = [r[0] for r in text_weights_token[0:x]]
    else:
        x = min(len(text_weights_token),15)
        text = [r[0] for r in text_weights_token[0:x]]

    for i in range(len(text)):
        if text[i].isalpha():
            text[i] =  text[i].lower()

    return text

def passDictionary(words):
    dictionary = Dictionary.objects.all()
    ids = []
    
    for word in words:
        bool =  Dictionary.objects.filter(text=word).exists()

        if not bool:
            Dictionary.objects.create(text = word)

        id=Dictionary.objects.get(text=word).id
        ids.append(id)

    return ids
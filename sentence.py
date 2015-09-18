#coding:utf-8
import config, util
from connective import Connective
from connective_dict import Connectives_dict

class Sentence:
    def __init__(self, DocID, paragIndex, tokens, sent_index, doc_indices, pos_tags, parsetree, dependencies):
        self.DocID = DocID
        self.paragIndex = paragIndex
        self.tokens = tokens
        self.sent_index = sent_index
        self.doc_indices = doc_indices
        self.pos_tags = pos_tags
        self.parsetree = parsetree
        self.dependencies = dependencies
        self.connectives = [] #连接词列表

        #在sentence中标注连接词，[([2,6], 'for instance'), ....]
        for token_indices, conn_name in check_connectives(self.tokens):
            self.connectives.append(Connective(self.DocID, self.sent_index, token_indices, conn_name))




''' 识别sentence中的连接词, 返回识别出来的连接词的indices #[([2,6], 'for instance'), ....] '''
def check_connectives(sent_tokens):
    sent_tokens = [ word.lower() for word in sent_tokens ]
    indices = []
    tagged = set([])#已经标记列表
    sortedConn = Connectives_dict().sorted_conns_list
    for conn in sortedConn:
        #判断连接词是否在句子中出现
        if '..' in conn:#对于这种类型的在sentence中只识别一次
            c1, c2 = conn.split('..')
            c1_indice = util.getSpanIndecesInSent(c1.split(), sent_tokens)#[[7]]
            c2_indice = util.getSpanIndecesInSent(c2.split(), sent_tokens)#[[10]]
            if c1_indice!= [] and c2_indice != []:#词在句子中
                if c1_indice[0][0] < c2_indice[0][0]:#c1,c2 的先后顺序也不能错
                    #识别到该连接词
                    temp = set([t for t in (c1_indice[0]+c2_indice[0]) ])
                    #判断连接词是否已经被识别过了，如 已经识别了 for example 就不用去识别for 了
                    if tagged & temp == set([]):#没有被识别过，加入indices，加入tagged
                        indices.append((c1_indice[0]+c2_indice[0], conn))# [[7], [10]]
                        tagged = tagged.union(temp)
        else:
            c_indice = util.getSpanIndecesInSent(conn.split(), sent_tokens)#[[2,6],[1,3],...]
            if c_indice !=[]:
                #检查c_indice中每一项，如果该项在tagged中存在，剔除该项
                tt = []
                for item in c_indice:
                    if set(item) & tagged == set([]):
                        tt.append(item)
                c_indice = tt

                if c_indice != []:
                    indices.extend([(item, conn) for item in c_indice])#[([2,6], 'for instance'), ....]
                    tagged = tagged.union(set([r for t in c_indice for r in t]))
    return indices


#从raw text获取paragraph信息，从conn_format 获取tokens, sent_index, doc_indices, pos_tags
#从parse json 获取parsetree, dependencies,


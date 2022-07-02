# -*- coding: utf-8 -*-
"""
Created on Fri May 13 14:55:17 2016

@author: phdlab
"""
def readGIZA(giza_file_dir):
    with open(giza_file_dir, encoding = 'utf8') as f:
        lines = f.readlines()
        index = 0
        src_sent = []
        trg_sent = []
        src_trg = []
        while (index < len(lines)):
            token_list_1 = lines[index+1]
            token_list_2 = (lines[index+2].strip()).split()
            trg = token_list_1.strip()
            src = []
            aligned = []
            flag = False
            for token in token_list_2:
                if True == flag: 
                    if '({' == token:
                        correspond_token_list = []
                    elif '})' == token:
                        flag = False
                        aligned.append(correspond_token_list)
                    else:
                        correspond_token_list.append(int(token))
                else:
                    flag = True
                    src.append(token)
            src = ' '.join(src)
            src_sent.append(src)
            trg_sent.append(trg)
            src_trg.append(aligned)
            index += 3
        return src_sent, trg_sent, src_trg
def writeELicitation(eli_file_dir, src_sent, trg_sent, src_trg):
    output ='encoding: UTF8\nsrclang: English\ntgtlang: Vietnamese\n\n'
    for i in range(len(src_sent)):
        output += 'newpair\n'
        output += 'srcsent: ' + src_sent[i] + '\n'
        output += 'tgtsent: ' + trg_sent[i] + '\n'
        tmp = src_trg[i]
        align = []
        for j in range(len(tmp)):
            align += [(j+1, ele) for ele in tmp[j] if tmp[j] != []]
        align = (str(pair) for pair in align) 
        align = ','.join(align)
        align = align.replace(' ','')
        output += 'aligned: ' + '(' + align + ')\n'
        output += 'context:\ncomment:\n\n'
    with open(eli_file_dir, 'w', encoding = 'utf8') as f:
        f.write(output)
def readElicitation(eli_file_dir):
    with open(eli_file_dir, encoding = 'utf8') as f:
        lines = f.readlines()
    index = 5
    src_sent = []
    trg_sent = []
    src_trg = []
    while (index < len(lines)):
        src = (((lines[index]).strip()).split())[1:]
        trg = (((lines[index+1]).strip()).split())[1:]
        tmp = ((lines[index+2]).strip())
        tmp = tmp.split(' ', 1)
        tmp = tmp[1][1:-1]      
        align = [[] for i in range(len(src)+1)]
        tmp = tmp.replace('(', ' ')
        tmp = tmp.replace(')', ' ')
        tmp = tmp.replace(',', ' ')
        tmp = tmp.split()
        subindex = 0
        while (subindex < len(tmp)):
            align[int(tmp[subindex])].append(int(tmp[subindex+1]))
            subindex+=2
        trg = ' '.join(trg)
        src_sent.append(src)
        trg_sent.append(trg)
        src_trg.append(align)
        index += 7
    return src_sent, trg_sent, src_trg
def writeGIZA(giza_file_dir, src_sent, trg_sent, src_trg):
    output = ''
    for i in range(len(src_sent)):
        output += '# Sentence pair ('+str(i+1)+')\n'
        output += trg_sent[i]+'\n'
        align = ''
        src = src_sent[i]
        tmpalign = src_trg[i]
        for j in range(len(src)): 
            align += src[j] + ' ({ '
            tmp = [str(k) for k in tmpalign[j+1]]
            align += ' '.join(tmp)
            align += ' }) '
        align += '\n'
        output += align
    with open(giza_file_dir, 'w', encoding = 'utf8') as f:
        f.write(output)        
def convert2Eli(giza_file_dir, eli_file_dir):
    srcsent, tgtsent, src_trg = readGIZA(giza_file_dir)
    writeELicitation(eli_file_dir, srcsent, tgtsent, src_trg) 
def convert2GIZA(eli_file_dir, giza_file_dir):    
    src_sent, trg_sent, src_trg = readElicitation(eli_file_dir)
    writeGIZA(giza_file_dir, src_sent, trg_sent, src_trg)
    
if __name__ == '__main__':
    #convert2Eli('result.A3.final', 'eli.txt')
    convert2GIZA('eli.txt', 'giza.txt')
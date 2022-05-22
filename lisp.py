istr = "((A=2&&B=3)||(C=4&&D=5))"
print(istr)

def parser(tstr, oj={}):
    ts, jd, pval = None, None, None
    istr = tstr
    while istr:
        print("istr: ", istr)
        tl = []
        for i, s in enumerate(istr):
            if s == '(':
                ts = i
                if tl:
                    jd = tmp_eval(''.join(tl))
                    oj.setdefault(jd, []).append(pval)
                    tl = []
                    pval = None
            elif s == ')':
                jd = tmp_eval(''.join(tl))
                if pval:
                    oj.setdefault(jd, []).append(pval)
                pval = jd
                istr = istr[:ts] + istr[i+1:]
                istr.strip()
                break
            else:
                tl.append(s)
        if len(istr)<=4:
            break
    print({'query':oj})

def tmp_eval(sstr='', d={}):
    sstr = sstr.strip()
    if sstr == '||': return 'or'
    if sstr == '&&': return 'and'
    alst = sstr.split('&&')
    if len(alst) >1:
        d['and'] = {}
        td = {}
        for each in alst:
            blst = each.strip().split("||")
            for e in blst:
                k, v = e.split('=')
                td[k.strip()] = int(v.strip())
        if len(blst) >1:
            print '--->',d

            d['and']['or'] = td
        else:
            d['and'] = td
        return d
    else:
        print '--->',d

        d['or'] = {}
        td = {}
        for each in alst:
            blst = each.strip().split("&&")
            for e in blst:
                k, v = e.split('=')
                td[k.strip()] = int(v.strip())
        if len(blst) >1:
            d['or']['and'] = d.setdefault('or',[]).append(td)
        else:
            d['or'] = d.setdefault('or',[]).append(td)
        return d

parser(istr)

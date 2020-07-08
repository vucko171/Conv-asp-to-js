import re
import sys
import os.path
def convert(data,picked,picked1):
    options = ["change vars, dims, and some functions", "if, function, for, while", "comment comments",	
           "convert stored procedure", "HTML", "remove multiline '_'(not included in all)", "err raise(not included in all)", "all"]	
    options1 = ["if", "triple equals and doesn't equal", "functions", "loops", "Select Case", "return", "all"]
    inJS = 0
    inHTML = 0
    inCom = 0
    fNames = []
    check = []
    oVB = []
    cVB = []
    comment = [r'(?:(<!--)|(-->))', r'(?:(\s?<%)|(%>))']
    findLastTag=0
    for x in range(len(data)):
        if re.search(r'^\s*<(?!%|!--)(?!script|\/script).*?(?<!%)>',data[x], flags=re.I):
            findLastTag=x
    for x in range(len(data)):
        if x >= len(data):
            break
        for match in reversed(list(re.finditer(r'<script .*?>', data[x], flags=re.I))):
            if len(re.findall(r'(?<!\\)"', data[x][:match.start()])) % 2 == 0 and len(re.findall(r"(?<!\\)'", data[x][:match.start()])) % 2 == 0:
                inJS = 1
        for match in reversed(list(re.finditer(r'</script>', data[x], flags=re.I))):
            if len(re.findall(r'(?<!\\)"', data[x][:match.start()])) % 2 == 0 and len(re.findall(r"(?<!\\)'", data[x][:match.start()])) % 2 == 0:
                inJS = 0
        if not inHTML:
            if 2 in picked or len(options)-1 in picked:
                data[x] = re.sub(r'^(\s*)(<%|%>)', r"\1//\2 <---Ivan comment", data[x], flags=re.I)
            for match in reversed(list(re.finditer(r'(<%|%>)', data[x], flags=re.I))):
                if data[x][match.start():match.end()] == "<%":
                    oVB.append([x, match.start()])
                else:
                    cVB.append([x, match.start()])
            if 2 in picked or len(options)-1 in picked:
                for match in reversed(list(re.finditer(r'(<script (?:[^>](?!src))*?>)', data[x], flags=re.I))):
                    if len(re.findall(r'(?<!\\)"', data[x][:match.start()])) % 2 == 0 and len(re.findall(r"(?<!\\)'", data[x][:match.start()])) % 2 == 0:
                        data[x] = re.sub(r'(<script (?:[^>](?!src))*?>)', r'{', data[x], flags=re.I)
                for match in reversed(list(re.finditer(r'</script>', data[x], flags=re.I))):
                    if len(re.findall(r'(?<!\\)"', data[x][:match.start()])) % 2 == 0 and len(re.findall(r"(?<!\\)'", data[x][:match.start()])) % 2 == 0:
                        data[x] = re.sub(r'(</script>)', r'}', data[x], flags=re.I)
                if "<!--" in data[x]:
                    print(x,inJS,data[x])
                data[x] = re.sub(r'(<!--.*)', r'/*\1'*inJS + r'{/*\1'*((inJS+1)%2), data[x], flags=re.I)
                data[x] = re.sub(r'(.*-->)', r'\1*/'*inJS + r'\1*/}'*((inJS+1)%2), data[x], flags=re.I)
            # or (oVB[-1][0] == cVB[-1][0] and oVB[-1][1] > cVB[-1][1]):
            if len(oVB) != 0 and len(cVB) != 0 and oVB[-1][0] == cVB[-1][0] and oVB[-1][0] == x:
                # deal with same line VB change
                if 2 in picked or len(options)-1 in picked:
                    data[x] = "//"+data[x]
            elif not inJS and len(oVB) != 0 and (len(cVB) == 0 or oVB[-1][0] > cVB[-1][0]) and not re.search(r'\/\/', data[x]):
                if 2 in picked or len(options)-1 in picked:
                    data[x] = re.sub(r'^(\s*)\'', r"\1//'", data[x], flags=re.I)
                    data[x] = re.sub(r'^(\s*)(Option\s*Explicit)', r"\1//\2 <---Ivan comment", data[x], flags=re.I)
                    data[x] = re.sub(r'^(\s*)(Response.Expires\s*=\s*-1)', r"\1//\2 <---Ivan comment", data[x], flags=re.I)
                    data[x] = re.sub(r'^(\s*)(Response.Buffer\s*=\s*true)', r"\1//\2 <---Ivan comment", data[x], flags=re.I)
                if not re.search(r'\/\/', data[x]):
                    if 4 in picked1 or len(options1)-1 in picked1 or len(options)-1 in picked:
                        data[x] = re.sub(r'Select Case (.*?)\n', r'switch(\1) {\n', data[x], flags=re.I)
                        data[x] = re.sub(r'Case Else', r'default:', data[x], flags=re.I)
                        data[x] = re.sub(r'Case (.*?)\n', r'case \1:\n', data[x], flags=re.I)
                        data[x] = re.sub(r'^(\s*)end Select\s*\n', r'\1}\n', data[x], flags=re.I)
                    if 2 in picked or len(options)-1 in picked:
                        data[x] = re.sub(r'(on error.*)', r'//\1 <---Ivan comment', data[x], flags=re.I)
                        data[x] = re.sub(r'Exit(.*)', r'//Exit\1 <---Ivan comment', data[x], flags=re.I)
                        data[x] = re.sub(r"((?:[^'\n]|(?<=\w)')*)(?:(?<!\w)')((?:[^'\n\"]|(?<=\w)')*)$",
                                        r"\1//'\2", data[x], flags=re.I)
                    if 1 in picked or len(options)-1 in picked:
                        if 0 in picked1 or len(options1)-1 in picked1 or len(options)-1 in picked:
                            while re.search(r'if\s(.*?)_\s*$', data[x], flags=re.I):
                                data[x] += data[x+1]
                                data.pop(x+1)
                                findLastTag-=1
                                data[x] = re.sub(r'if\s(.*?)_\s*\n\s+', r'if \1 ', data[x], flags=re.I)
                        if 1 in picked1 or len(options1)-1 in picked1 or len(options)-1 in picked:
                            while re.search(r'if(.*?[^=<>])=([^=<>].*?)then', data[x], flags=re.I):
                                data[x] = re.sub(r'if(.*?[^=<>])=([^=<>].*?)then', r'if\1 === \2then', data[x], flags=re.I)
                            while re.search(r'<>', data[x], flags=re.I):
                                data[x] = re.sub(r'<>', r'!==', data[x], flags=re.I)
                        if 0 in picked1 or len(options1)-1 in picked1 or len(options)-1 in picked:
                            data[x] = re.sub(r'if\s+(.*?then)', r'if (\1', data[x], flags=re.I)
                            data[x] = re.sub(r'(if \(.*?)then', r'\1){', data[x], flags=re.I)
                            data[x] = re.sub(r'Elseif', r'} if', data[x], flags=re.I)
                            data[x] = re.sub(r'Else', r'} else {', data[x], flags=re.I)
                            data[x] = re.sub(r'^(\s*)end if\s*\n', r'\1}\n', data[x], flags=re.I)
                            data[x] = re.sub(r'If', r'if', data[x], flags=re.I)
                            data[x] = re.sub(r' New ', r' new ', data[x], flags=re.I)
                        if 2 in picked1 or len(options1)-1 in picked1 or len(options)-1 in picked:
                            data[x] = re.sub(r'^(\s*)Sub', r'\1function', data[x], flags=re.I)
                            data[x] = re.sub(r'Function', r'function', data[x], flags=re.I)
                            data[x] = re.sub(r'function(.*?\))', r'function\1{', data[x], flags=re.I)
                            data[x] = re.sub(r'^(\s*)end function\s*\n', r'\1}\n', data[x], flags=re.I)
                        if 3 in picked1 or len(options1)-1 in picked1 or len(options)-1 in picked:
                            data[x] = re.sub(r'^(\s*)Class\s*(.*?)\s*\n', r'\1class \2{\n', data[x], flags=re.I)
                            data[x] = re.sub(r'^(\s*)for (.*)\n', r'\1for (\2){\n', data[x], flags=re.I)
                            # data[x] = re.sub(r'UBound\((.*?),\s*2\)', r'\1.length', data[x], flags=re.I)
                            data[x] = re.sub(r'for \(\s*(\w+)\s*=\s*(\d+)\s*to\s*(.*?)\){',
                                            r'for (\1 = \2; \1 < \3; \1++){', data[x], flags=re.I)
                            data[x] = re.sub(r'^(\s*)next', r'\1}', data[x], flags=re.I)
                            data[x] = re.sub(r'do until (.*)', r'while(!\1){', data[x], flags=re.I)
                            data[x] = re.sub(r'while (.*)', r'while(!\1){', data[x], flags=re.I)
                            data[x] = re.sub(r'^(\s*)(?:Wend|End Class|End Sub)\s*\n', r'\1}\n', data[x], flags=re.I)
                            data[x] = re.sub(r'loop', r'}', data[x], flags=re.I)
                        if 5 in picked1 or len(options1)-1 in picked1 or len(options)-1 in picked:
                            for fName in range(len(fNames)):
                                if check[fName] == 0 and re.search(r'^(\s*).*?'+fNames[fName]+r'\s*=\s*(.*)', data[x], flags=re.I):
                                    data[x] = re.sub(r'^(\s*).*?('+fNames[fName]+r')\s*=\s*(.*)',
                                                    r'\1var \2 = \3', data[x], flags=re.I)
                                    check[fName] = 1
                            match = re.match(r'.*function\s*(.*?)\s*\(', data[x], flags=re.I)
                            if match and match.group(1) not in fNames:
                                fNames.append(match.group(1))
                                check.append(0)
                            data[x] = re.sub(r'(CreateParameter\(.*,)\s*,', r'\1 null,', data[x], flags=re.I)

                    if 5 in picked:
                        while re.search(r'\s*_\s*$', data[x], flags=re.I):
                            data[x] += data[x+1]
                            data.pop(x+1)
                            findLastTag-=1
                            data[x] = re.sub(r'\s*_\s*\n\s*', r'', data[x], flags=re.I)
                    if 0 in picked or len(options)-1 in picked:
                        data[x] = re.sub(r'^(\s*)Dim\s+', r'\1var ', data[x], flags=re.I)
                        data[x] = re.sub(r'^(\s*)Set\s+', r'\1var ', data[x], flags=re.I)
                        data[x] = re.sub(r'^(\s*)Const\s+', r'\1const ', data[x], flags=re.I)
                        data[x] = re.sub(r'Cstr\(', r'String(', data[x], flags=re.I)
                        data[x] = re.sub(r'isArray\(', r'Array.isArray(', data[x], flags=re.I)
                        data[x] = re.sub(r'len\((.*?)\)', r'\1.length', data[x], flags=re.I)
                        data[x] = re.sub(r'replace\((.*?),', r'\1.replace(', data[x], flags=re.I)
                        data[x] = re.sub(r'mid\((.*?),(.*?),(.*?)\)', r'\1.slice(\2-1,\3)', data[x], flags=re.I)
                        data[x] = re.sub(r'=\s*nothing', r'= null', data[x], flags=re.I)
                    # data[x] = re.sub(r'getrows\(\)', r'rows', data[x], flags=re.I)
                    # data[x] = re.sub(r'\s+(\w+)=([^"]\w*)', r' \1={"\2"}', data[x], flags=re.I)
                    if 3 in picked or len(options)-1 in picked:
                        data[x] = re.sub(r'(\s*).*?\.Parameters\.Append (.*?)\s*\n', r'\1\2\n', data[x], flags=re.I)
                        data[x] = re.sub(r'\.Open\s+(.*?)\s*\n', r'.Open(\1)\n', data[x], flags=re.I)
                        data[x] = re.sub(r'\.Execute\s*(.*?)\s*\n', r'.Execute(\1)\n', data[x], flags=re.I)
                        data[x] = re.sub(r'Server\.CreateObject\(("ADODB.Command"|"ADODB.RecordSet")\)',
                                        r'new CallStoredProcedure()', data[x], flags=re.I)
                        data[x] = re.sub(r'\.CreateParameter\((.*?),.*?,\s*adParamInput\s*,.*?,(.*?)\)\s*\n', r'.CreateParameter(\1,\2)\n', data[x], flags=re.I)
                        if re.search(r'\s*.*?\.CreateParameter\(.*?adParamOutput.*?\)\s*\n', data[x], flags=re.I):
                            findLastTag-=1
                            data.pop(x)
                        data[x] = re.sub(
                                r'(CommandText\s*=\s*")\{call\s*(JAGORA\..*?)\(\?(?:,\?)*\)\}"', r'\1\2"', data[x], flags=re.I)
                        data[x] = re.sub(r'(\s*.*?)\.Parameters\((.*?)\)',r'\1.Parameters[\2]', data[x], flags=re.I)
                    if 6 in picked:
                        while re.search(r'Err\.Raise.*\s*_\s*$', data[x], flags=re.I):
                            data[x] += data[x+1]
                            data.pop(x+1)
                            findLastTag-=1
                            data[x] = re.sub(r'(Err\.Raise.*)\s*_\s*\n\s*', r'\1', data[x], flags=re.I)
                        data[x] = re.sub(r'Err\.Raise (\d+).*?,(?:.*?(")(.*?)(").*?|(.*?)),(.*?)\n',
                                        r'throw new Error("\1" + \2 \3 \4\5 + \6)\n', data[x], flags=re.I)
                        data[x] = re.sub(r'Err\.Raise (\w+).*?,(?:.*?(")(.*?)(").*?|(.*?)),(.*?)\n',
                                        r'throw new Error(\1 + \2 \3 \4\5 + \6)\n', data[x], flags=re.I)
                        data[x] = re.sub(r'Err\.Description', r'Err.message', data[x], flags=re.I)
                    data[x] = re.sub(r'\s*_\s*\n', r'\n', data[x], flags=re.I)
                    matches = re.finditer(r'<\/?\w+', data[x], flags=re.I)
                    for match in reversed(list(matches)):
                        start, end = match.start(), match.end()
                        data[x] = data[x][:start]+data[x][start:end].lower()+data[x][end:]
                    for typ in [r'input', r'base', r'link', r'br', r'hr']:
                        # <input(([^<>]|%>|<%)*[^%\/])>
                        data[x] = re.sub(r'<'+typ+r'(([^<>]|%>|<%)*[^%\/])>', r'<'+typ+r'\1/>', data[x])
                    # finding matches not in string
                    inArr = [r'not\s',  r'&', r'(\s+)and(\s+)', r'(\s+)or(\s+)',
                            r'trim\((.*?\(.*?\(.*?\).*?\).*?|.*?\(.*?\).*?|.*?)\)']
                    outArr = [r'!', r'+', r' && ', r' || ',  r'\1.trim()']
                    for i in range(len(inArr)):
                        if len(options)-1 in picked or (i == 4 and 0 in picked or i != 4 and 1 in picked):
                            matches = re.finditer(inArr[i], data[x], flags=re.I)
                            for match in reversed(list(matches)):
                                start, end = match.start(), match.end()
                                if len(re.findall(r'(?<!\\)"', data[x][:match.start()])) % 2 == 0 and len(re.findall(r"(?<!\\)'", data[x][:match.start()])) % 2 == 0:
                                    data[x] = data[x][:start]+re.sub(inArr[i], outArr[i], data[x]
                                                                    [start:end], flags=re.I)+data[x][end:]
            if re.search(r'^\s*<(?!scr).*>', data[x], flags=re.I):
                inHTML = 1
                inJS = 0
                print("in",x,data[x])
        if findLastTag==x:
            inHTML = 0
            print("out",x,data[x])
        if 4 in picked or len(options)-1 in picked:
            if inHTML:
                for match in reversed(list(re.finditer(r'<script [^>]*?src[^>]*?>(.*?)</script>', data[x], flags=re.I))):
                    if len(re.findall(r'(?<!\\)"', data[x][:match.start()])) % 2 == 0 and len(re.findall(r"(?<!\\)'", data[x][:match.start()])) % 2 == 0:
                        data[x] = re.sub(r'(<script [^>]*?src[^>]*?)(>.*?)</script>', r'\1/\2', data[x], flags=re.I)
                data[x] = re.sub(r'<script (?:[^>](?!src))*?>', r'{', data[x], flags=re.I)
                data[x] = re.sub(r'</script>', r'}', data[x], flags=re.I)
                matches = re.finditer(r'<\/?\w+', data[x], flags=re.I)
                for match in matches:
                    start, end = match.start(), match.end()
                    data[x] = data[x][:start]+data[x][start:end].lower()+data[x][end:]
                buffer = 0
                bufferReleasable = []
                doneMatch = False
                for com in range(len(comment)):
                    doneCom = False
                    matches = re.finditer(comment[com], data[x], flags=re.I)
                    matches = [m for m in matches]
                    for match in range(len(matches)):
                        bufferR = 0
                        for buf in bufferReleasable:
                            if buf[0] <= matches[match].start() <= buf[1]:
                                bufferR -= buf[2]
                            elif buf[1] <= matches[match].start():
                                bufferR += (4-inJS)*2
                        if com == 1 and not doneCom:
                            if match+1 < len(matches) and matches[match].start(1) != -1 and matches[match+1].start(2) != -1:
                                # and data[x].count("\"", 0, matches[match].start()+buffer + bufferR) % 2 == 1:
                                if re.search(r'<[^%]*$', data[x][:matches[match].start()+buffer + bufferR], flags=re.I):
                                    EOT = re.search(r'^.*?(?<!%)>(?:{.*})?', data[x]
                                                    [matches[match+1].end()+buffer + bufferR:], flags=re.I)

                                    if (EOT):
                                        data[x] = data[x][:matches[match].start()+buffer + bufferR]+data[x][matches[match+1].end()+buffer + bufferR:matches[match+1].end()+buffer + bufferR+EOT.end()] + \
                                            "/* "*inJS + "{/* "*((inJS+1) % 2) + data[x][matches[match].start()+buffer + bufferR:matches[match+1].end()+buffer + bufferR] + " */"*inJS + " */}"*((inJS+1) % 2) + \
                                            data[x][matches[match+1].end()+buffer + bufferR+EOT.end():]
                                        bufferReleasable.append([matches[match].start() + buffer + bufferR,
                                                                matches[match+1].end() + buffer + bufferR + EOT.end()-1,
                                                                len(data[x][matches[match].start() + buffer + bufferR:matches[match+1].end()+buffer + bufferR])])
                                        doneMatch = True
                            # if match+1 < len(matches) and matches[match].start(1) != -1 and matches[match+1].start(2) != -1:
                            #    if data[x].find("\"", matches[match].end()+buffer, matches[match+1].start()+buffer) != -1:
                            #        data[x] = "/* "*inJS + "{/* "*((inJS+1) % 2) + data[x][:-1] + \
                            #            " */\n"*inJS + " */}\n"*((inJS+1) % 2)
                            #        doneMatch = True
                            #        break
                        if (not doneMatch or com == 0):
                            if matches[match].start(1) != -1:
                                if com == 0:
                                    doneMatch = True
                                data[x] = data[x][:matches[match].start()+buffer] + \
                                    "/* "*inJS + "{/* "*((inJS+1) % 2) + \
                                    data[x][matches[match].start()+buffer:]
                                buffer += 4-inJS
                                inCom += 1
                            elif matches[match].start(2) != -1:
                                if com == 0:
                                    doneCom = True
                                if inCom == 1:
                                    data[x] = data[x][:matches[match].end()+buffer] + \
                                        " */"*inJS + " */}"*((inJS+1) % 2) + \
                                        data[x][matches[match].end()+buffer:]
                                    buffer += 4-inJS
                                if inCom < 1:
                                    print("something's wrong")
                                inCom -= 1
                for typ in [r'input', r'base', r'link', r'br', r'hr', r'img']:
                    # <input(([^<>]|%>|<%)*[^%\/])>
                    data[x] = re.sub(r'<'+typ+r'([^<]*)>',
                                    r'<'+typ+r'\1/>', data[x], flags=re.I)
                while re.search(r'(<[^>%]*?\w*=\s*)([^"\']\w*)', data[x], flags=re.I):
                    data[x] = re.sub(r'(<[^>%]*?\w*=\s*)([^"\']\w*)', r'\1"\2"', data[x], flags=re.I)
                matches = re.finditer(r'style="(.*?)"', data[x], flags=re.I)
                for match in matches:
                    temp = match.group(0).split('"')[1].split(";")
                    final = ""
                    for style in range(len(temp)):
                        temp2 = temp[style].lower().split(":")
                        if "-" in temp2[0]:
                            temp2[0] = temp2[0][:temp2[0].index(
                                "-")]+temp2[0][temp2[0].index("-")+1].upper()+temp2[0][temp2[0].index("-")+2:]
                        final += temp2[0]+":\""+temp2[1]+"\","
                    data[x] = data[x][:match.start()]+'style={{'+final[:-1]+"}}"+data[x][match.end():]
                data[x] = re.sub(r'cellpadding', r'cellPadding', data[x], flags=re.I)
                data[x] = re.sub(r'cellspacing', r'cellSpacing', data[x], flags=re.I)
                data[x] = re.sub(r'onclick', r'onClick', data[x], flags=re.I)
                data[x] = re.sub(r'TITLE', r'title', data[x], flags=re.I)

        #    if list(re.finditer("<html", data[x])):
        #        data[x] = data[x].replace('<html', 'return (\n <html')
        #        js = 0
        # data = ["import React from 'react';\nfunction Srt_ReqResult() {\n"]+data+[
        #    ")}\nexport default Srt_ordlookup;"]
    return data
if __name__ == "__main__":
    if len(sys.argv) > 1:
        f = sys.argv[1]
    else:
        f = str(input("please enter a file name"))

    if not os.path.exists(sys.argv[1]):
        print("\nno such file, please try another file\n")
        sys.exit()
    options = ["change vars, dims, and some functions", "if, function, for, while", "comment comments",
            "convert stored procedure", "HTML", "remove multiline '_'(not included in all)", "err raise(not included in all)", "all"]
    options1 = ["if", "triple equals and doesn't equal", "functions", "loops", "Select Case", "return", "all"]
    print("\nhow would you like to convert the file, enter a number from 0-" +
        str(len(options)-1)+" if multiple, enter comma seperated")
    for x in range(len(options)):
        print(x, options[x])
    picked = str(input("enter option here: ")).split(",")
    for x in range(len(picked)):
        if picked[x].isdigit() and int(picked[x]) >= 0 and int(picked[x]) < len(options):
            picked[x] = int(picked[x])
        else:
            print("\nenter a valid option\n")
            sys.exit()
    picked1 = []
    if 1 in picked:
        print()
        for x in range(len(options1)):
            print(x, options1[x])
        picked1 = str(input("enter option here: ")).split(",")
        for x in range(len(picked1)):
            if picked1[x].isdigit() and int(picked1[x]) >= 0 and int(picked1[x]) < len(options1):
                picked1[x] = int(picked1[x])
            else:
                print("\nenter a valid option\n")
                sys.exit()
    f = open(sys.argv[1], "r")
    data = f.readlines()
    f.close()

    data=convert(data,picked,picked1)

    f = open("test.js", "w+")
    f.writelines(data)
    f.close()
    print("\nwrote to file "+"test.js"+"\n")
    # else:
    #    print("\nplease specify a file to convert like:\npython ./conv3.py ./routines.inc\n")
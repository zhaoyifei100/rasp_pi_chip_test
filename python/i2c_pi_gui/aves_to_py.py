'''yfzhao init version'''


def replace_func_name(func_name):
    func_name_new=list(func_name)
    for i_func_name in range(len(func_name_new)):
        if(    (func_name_new[i_func_name]>='a' and func_name_new[i_func_name]<='z') \
            or (func_name_new[i_func_name]>='A' and func_name_new[i_func_name]<='Z') \
            or (func_name_new[i_func_name]>='0' and func_name_new[i_func_name]<='9') ):
            func_name_new[i_func_name]=func_name_new[i_func_name]
        elif(func_name[i_func_name]=="."):
            func_name_new[i_func_name]="p"
        else:
            func_name_new[i_func_name]="_"
    func_name_new="".join(func_name_new)
    return func_name_new

def remove_comment(block_lines):
    return_list=[]
    for line in block_lines:
        return_list.append(line.split(";")[0])
    return return_list

def convert_ref_name(block_lines):
    return_list = []
    for line in block_lines:
        if(line[0]=="i"):
            # sub function call
            call_func_name_old = line.strip().split('"')[-2]
            call_func_name_new = replace_func_name(call_func_name_old)
            return_list.append("REF;;SUB "+call_func_name_new)
        else:
            #delete " "
            return_list.append(line.replace(" ",""))
    return return_list

def get_func_block(lines):
    return_disc={}
    func_start_nm_list=[]
    func_end_nm_list=[]
    for nm, line in enumerate(lines):
        if (line[0] == ":" and line[-1] == ":"):
            func_start_nm_list.append(nm)
        elif (line=="End"):
            func_end_nm_list.append(nm)

    start_nm_len=len(func_start_nm_list)
    end_nm_len=len(func_end_nm_list)
    if(start_nm_len!=end_nm_len):
        print("Function & End not match, ERROR.")
        return

    for index, nm in enumerate(func_start_nm_list):
        #get func_name as disc key
        func_name_old = lines[nm].strip(":").strip(" ")
        func_name_new = replace_func_name(func_name_old)
        #get block line number
        block_start_nm=nm+1
        block_end_nm=func_end_nm_list[index]
        #get block lines
        block_lines=lines[block_start_nm:block_end_nm]
        #remove comments
        block_lines=remove_comment(block_lines)
        #include this
        block_lines=convert_ref_name(block_lines)
        #get return disc
        return_disc[func_name_new]=block_lines
    return return_disc

def aves_to_pydisc(file_path):
    print(f"file_path={file_path}")
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        #remove empty
        #remove ;start
        lines = [line.strip() for line in lines if line.strip() and not line.startswith(';')]
    '''debug use'''
    #for line in lines:
        #print(line)
    '''debug use'''
    #get all function name
    aves_block_disc=get_func_block(lines)
    #print(aves_block_disc)
    return aves_block_disc



if __name__ == '__main__':
    file_path = "H:\\gs_svn\\eval\\aves\\shared_scripts\\gsu1001_nto_scripts.txt"
    disc=aves_to_pydisc(file_path)
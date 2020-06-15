import os
import sys
import zlib 


def topo_order_commits():
    git_path = get_git_directory()  #get the git directory
    
    local_branch_files = []         #array with absolute path of branches 
    local_branch_hashes = {}        #dictionary that matches the absolute path to the hash value 

    #fill out the values
    get_local_branches(git_path + "/refs/heads", local_branch_files, local_branch_hashes)       

    #build the commit graph, return a dictionary of commit nodes and root hashes
    #commit_nodes matches a hash to a CommitNode object - sorted in function
    #root_hashes is just a sorted array of the hashes of root nodes - sorted in function
    commit_nodes, root_hashes = build_commit_graph(git_path, local_branch_files, local_branch_hashes)  

    #sort the nodes topoligically and return an order stack
    order = get_topo_ordered_commits(commit_nodes, root_hashes)

    #make a dictionary that matches hash values to an array of branch names
    head_to_branches = {}
    for entry in local_branch_files:
        hash_value = local_branch_hashes[entry]
        index = entry.find("/refs/heads/") + len("/refs/heads/")
        head_to_branches.setdefault(hash_value,[]).append(entry[index:])
    
    #print output
    print_topo_ordered_commits_with_branch_names(commit_nodes, order, head_to_branches)

    
class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()    
        self.children = set()


def print_topo_ordered_commits_with_branch_names(commit_nodes, topo_ordered_commits, head_to_branches):
    jumped = False
    for i in range(len(topo_ordered_commits)):
        commit_hash = topo_ordered_commits[i]
        if jumped:
            jumped = False
            sticky_hash = ' '.join(commit_nodes[commit_hash].children)
            print(f'={sticky_hash}')
        branches = sorted(head_to_branches[commit_hash]) if commit_hash in head_to_branches else []
        print(commit_hash + (' ' + ' '.join(branches) if branches else ''))
        if i+1 < len(topo_ordered_commits) and topo_ordered_commits[i+1] not in commit_nodes[commit_hash].parents:
            jumped = True
            sticky_hash = ' '.join(commit_nodes[commit_hash].parents)
            print(f'{sticky_hash}=\n')



def get_topo_ordered_commits(commit_nodes, root_hashes):
    order = []
    visited = set()
    stack = list(root_hashes.copy())
    children_not_processed = []
   
    while len(stack) != 0:
        v = stack.pop()
        if v in order:
            continue
            
        visited.add(v)
        
        children_not_processed.clear()
        for child in commit_nodes[v].children:
            if child not in visited:
                children_not_processed.append(child)
        
        if len(children_not_processed) == 0:
            order.append(v)
        else:
            stack.append(v)
            stack += children_not_processed

    return order



def build_commit_graph(git_path, local_branch_files, local_branch_hashes):
    commit_nodes = {}
    root_hashes = set()
    visited = set()
    stack = []
    for entry in local_branch_files:
        stack.append(local_branch_hashes[entry])


    while len(stack) != 0:
        commit_hash = stack.pop()
        if commit_hash in visited:
            continue 

        visited.add(commit_hash)
        if commit_hash not in commit_nodes:
            commit_nodes[commit_hash] = CommitNode(commit_hash) 
            

        object_file_path = git_path + "/objects/" + commit_hash[:2] + "/" + commit_hash[2:]
        if os.path.isfile(object_file_path):
            binary_contents = open(object_file_path, 'rb').read()
            decomp_contents = zlib.decompress(binary_contents).decode()
            contents_list = decomp_contents.split('\n')
        for line in contents_list:
            if "parent" in line:
                parent_hash_list = line.split(' ')
                if len(parent_hash_list) == 2: 
                    commit_nodes[commit_hash].parents.add(parent_hash_list[1])

        if len(commit_nodes[commit_hash].parents) == 0:
            root_hashes.add(commit_hash)


        for parent_hash in commit_nodes[commit_hash].parents:
            if parent_hash not in visited:
                stack.append(parent_hash)
            if parent_hash not in commit_nodes:
                commit_nodes[parent_hash] = CommitNode(parent_hash)
            commit_nodes[parent_hash].children.add(commit_hash)

    #sort the parents and children
    for node in commit_nodes:
        commit_nodes[node].children = sorted(commit_nodes[node].children)
        commit_nodes[node].parents = sorted(commit_nodes[node].parents)

    root_hashes = sorted(root_hashes)
    return commit_nodes, root_hashes


#recursive function to assemble a list with all files in it
#and a dictionary which uses said files to map to their hashes
def get_local_branches(path, local_branch_files, local_branch_hashes):
    #all entries under current directory
    heads = os.listdir(path)

    #check for files in entries and add to list and dictionary
    #if a directory, use recursion
    for entry in heads:
        entry_path = os.path.join(path, entry)

        if os.path.isfile(entry_path):
            f = open(entry_path, 'r')
            contents = f.read().replace('\n','')
            local_branch_files.append(entry_path)
            local_branch_hashes[entry_path] = contents

        elif os.path.isdir(entry_path):
            get_local_branches(entry_path, local_branch_files, local_branch_hashes)



def get_git_directory():
    curr_dir = os.getcwd()
    while True:
        #get all files in current directory
        files_in_curr_dir = os.listdir(curr_dir)
        
        #check if any are the .git directory
        for entry in files_in_curr_dir:
            if entry == ".git":
                return os.path.join(curr_dir, entry)


        os.chdir(os.pardir)  
        #get new directory and make sure its not root directory
        curr_dir = os.getcwd()
        if curr_dir == "/":
            print("Not inside a Git repository", file=sys.stderr)
            exit(1)



if __name__ == "__main__":
    topo_order_commits() 

    
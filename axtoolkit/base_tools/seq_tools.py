class SeqTools:
    def __init__(self):
        pass

    def read_fasta(file_path):
        '''read a fasta file return the fasta dic contain seq and length of the seq
        Args:
            file_path: the path of the fasta file
        Returns:
            fasta_dict: a dictionary contain the seq and length of the seq, the key is the sequence name
        Example:
            >>> read_fasta('example.fasta')
            {'seq1': {'sequence': 'ATCG', 'length': 4},'seq2': {'sequence': 'ATCG', 'length': 4}}
        '''
        fasta_dict = {}
        with open(file_path, 'r') as file:
            sequence_name = None
            sequence = ''
            for line in file:
                line = line.strip()
                if line.startswith('>'):
                    if sequence_name:
                        # 保存上一个序列的信息
                        fasta_dict[sequence_name] = {'sequence': sequence, 'length': len(sequence)}
                    # 新的序列开始
                    sequence_name = line[1:]  # 去掉描述行的'>'
                    sequence = ''
                else:
                    sequence += line
            # 保存最后一个序列的信息
            if sequence_name:
                fasta_dict[sequence_name] = {'sequence': sequence, 'length': len(sequence)}
        return fasta_dict
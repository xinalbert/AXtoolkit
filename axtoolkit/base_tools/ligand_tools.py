from rdkit import Chem 


class Ligandkit:
    def __init__(self):
        pass
    def sdf_to_smiles(sdf_file:str, smiles_file:str)->None:
        """
        Args:
            sdf_file: sdf file path
            smiles_file: smiles file path
        Returns:
            smiles_file: smiles file path
        Example:
            >>> sdf_to_smiles('test.sdf', 'test.smi')
        Note:
            sdf_file and smiles_file should have the same name with different suffixes.
        """
        suppl = Chem.SDMolSupplier(sdf_file)
        with open(smiles_file, 'w') as f:
            for mol in suppl:
                if mol is not None:
                    smiles = Chem.MolToSmiles(mol)
                    f.write(smiles+'\n')
        return smiles_file


    def sdf_to_smiles_large_file(sdf_file: str, smiles_file: str) -> None:
        """
        Convert a large SDF file to SMILES format, optimizing memory usage.

        Args:
            sdf_file: Path to the input SDF file.
            smiles_file: Path to the output SMILES file.

        Example:
            >>> sdf_to_smiles_large_file('large_molecules.sdf', 'large_molecules.smi')
        """
        # Using SDMolSupplier as a generator to handle large files efficiently
        suppl = Chem.SDMolSupplier(sdf_file)
        with open(smiles_file, 'w') as f:
            for mol in suppl:
                if mol is not None:
                    smiles = Chem.MolToSmiles(mol)
                    f.write(smiles + '\n')
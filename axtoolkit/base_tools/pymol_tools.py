from pymol import cmd, CmdException, util
def init_pymol():
    cmd.reinitialize()
    cmd.bg_color("white")
    cmd.set("ambient", 0.4)
    cmd.set("ambient_occlusion_mode", 1)
    cmd.set("antialias", 2)
    cmd.set("ortho", 1) 
    cmd.set("ray_trace_mode", 0)
    cmd.set("orthoscopic", 1)
    cmd.delete('all')
    cmd.set('label_color', 'blue')
    cmd.set("cartoon_transparency", 0.6)

##### the fllowing function is get from pymol-users mailing list, and modified by me to fit my need.

def get_raw_distances(names='', state=1, selection='all', quiet=1):
    '''
DESCRIPTION

    Get the list of pair items from distance objects. Each list item is a
    tuple of (index1, index2, distance).

    Based on a script from Takanori Nakane, posted on pymol-users mailing list.
    http://www.mail-archive.com/pymol-users@lists.sourceforge.net/msg10143.html

ARGUMENTS

    names = string: names of distance objects (no wildcards!) {default: all
    measurement objects}

    state = integer: object state {default: 1}

    selection = string: atom selection {default: all}

SEE ALSO

    select_distances, cmd.find_pairs, cmd.get_raw_alignment
    '''
    from chempy import cpv

    state, quiet = int(state), int(quiet)
    if state < 1:
        state = cmd.get_state()

    valid_names = cmd.get_names_of_type('object:measurement')
    if names == '':
        names = ' '.join(valid_names)
    else:
        for name in names.split():
            if name not in valid_names:
                print(' Error: no such distance object: ' + name)
                raise CmdException

    raw_objects = cmd.get_session(names, 1, 1, 0, 0)['names']

    xyz2idx = {}
    cmd.iterate_state(state, selection, 'xyz2idx[x,y,z] = (model,index)',
                      space=locals())

    r = []
    for obj in raw_objects:
        try:
            points = obj[5][2][state - 1][1]
            if points is None:
                raise ValueError
        except (KeyError, ValueError):
            continue
        for i in range(0, len(points), 6):
            xyz1 = tuple(points[i:i + 3])
            xyz2 = tuple(points[i + 3:i + 6])
            try:
                r.append((xyz2idx[xyz1], xyz2idx[xyz2], cpv.distance(xyz1, xyz2)))
                if not quiet:
                    print(' get_raw_distances: ' + str(r[-1]))
            except KeyError:
                if quiet < 0:
                    print(' Debug: no index for %s %s' % (xyz1, xyz2))
    return r


def select_distances(names='', name='sele', state=1, selection='all', cutoff=-1, quiet=1):
    '''
DESCRIPTION

    Turns a distance object into a named atom selection.

ARGUMENTS

    names = string: names of distance objects (no wildcards!) {default: all
    measurement objects}

    name = a unique name for the selection {default: sele}

SEE ALSO

    get_raw_distances
    '''
    state, cutoff, quiet = int(state), float(cutoff), int(quiet)

    sele_dict = {}
    distances = get_raw_distances(names, state, selection)
    for idx1, idx2, dist in distances:
        if cutoff <= 0.0 or dist <= cutoff:
            sele_dict.setdefault(idx1[0], set()).add(idx1[1])
            sele_dict.setdefault(idx2[0], set()).add(idx2[1])

    cmd.select(name, 'none')
    tmp_name = cmd.get_unused_name('_')

    r = 0
    for model in sele_dict:
        cmd.select_list(tmp_name, model, list(sele_dict[model]), mode='index')
        r = cmd.select(name, tmp_name, merge=1)
        cmd.delete(tmp_name)

    if not quiet:
        print(' Selector: selection "%s" defined with %d atoms.' % (name, r))
    return r


def get_region_hbonds(docked_mol):
    hbonds = cmd.find_pairs(docked_mol,'receptor', cutoff = 3.5, angle = 20 )
    res_pos_dic = {}
    for bond in hbonds:
        atom1, atom2 = bond
        resi2, resn2 = cmd.get_model(f"index {atom2[1]}").atom[0].resi, cmd.get_model(f"index {atom2[1]}").atom[0].resn
        res_pos_dic[resn2] = resi2
    for res,pos in res_pos_dic.items():
        cmd.show('sticks',f"resi {pos}")
        cmd.label(f"resi {pos} and name CA", '"%s-%s" % (resn, resi)') # show the residue number of the receptor
        # cmd.label(f"resi {pos} and name CA", "resi") # show the residue number of the receptor again to make it more visible
        cmd.color("yellow", f"resi {pos}") # color the residue number of the receptor red
    return res_pos_dic

#####

def get_core_pep(core_seq):
    """
    This function gets the core peptide sequence from the docked protein.
    Args:
        core_seq (str): The core peptide sequence.
    Returns:
        int: The number of residues in the core peptide sequence.

    """
    cmd.select('core', f'pepseq {core_seq}')
    core_res = set()
    hd_res  = set()
    cmd.iterate('core', 'core_res.add((resn,resi))', space={'core_res': core_res})
    cmd.iterate('highlighted_residues_1', 'hd_res.add((resn,resi))', space={'hd_res': hd_res})
    core_res = [f"{resn}{resi}" for resn,resi in core_res]
    hd_res = [f"{resn}{resi}" for resn,resi in hd_res]
    core_res_count = 0
    res_cor_l = []
    for res in hd_res:
        if res in core_res:
            core_res_count += 1
            res_cor_l.append(res)
    cmd.select('none')
    return core_res_count, res_cor_l
    
            


def detect_hbonds(prot1, prot2, max_dist=3.5):
    """
    This function detects hydrogen bonds between two proteins.
    Args:
        prot1 (str): The first protein.
        prot2 (str): The second protein.
        max_dist (float): The maximum distance between two atoms to be considered as a hydrogen bond.
    Returns:
        None. The function only shows the hydrogen bonds on PyMOL.
    """
    # 1. add hydrogens to the proteins
    cmd.h_add(prot1)
    cmd.h_add(prot2)

    # 2. define the donors and acceptors
    cmd.select("don", "(elem n or elem o) and (neighbor hydro)")
    cmd.select("acc", "(elem o or (elem n and not (neighbor hydro)))")

    # 3. plot the hydrogen bonds
    cmd.distance("HBA", f"({prot1}) and acc", f"({prot2}) and don", max_dist)  # prot1受体到prot2供体
    cmd.distance("HBD", f"({prot1}) and don", f"({prot2}) and acc", max_dist)  # prot1供体到prot2受体

    # 4. remove the temporary selections
    cmd.delete("don")
    cmd.delete("acc")

    # 5. hide the hydrogens
    cmd.hide("everything", "hydro")

def show_hdbonds(prot1, prot2):
    """
    This function shows the hydrogen bonds between two proteins.
    Args:
        prot1 (str): The first protein.
        prot2 (str): The second protein.
        max_dist (float): The maximum distance between two atoms to be considered as a hydrogen bond.
        Returns:
        None. The function only shows the hydrogen bonds on PyMOL.
    """
    detect_hbonds(prot1, prot2)
    select_distances('HBA', 'HBA_s')
    select_distances('HBD', 'HBD_s')
     # 1. get the residue numbers of the hydrogen bonds
    residues = set()
    cmd.iterate('HBA_s', 'residues.add((resn, resi))', space={'residues': residues})
    cmd.iterate('HBD_s', 'residues.add((resn, resi))', space={'residues': residues})

    # 2. build the selection string for the highlighted residues
    selection = " or ".join([f"(resn {resn} and resi {resi})" for resn, resi in residues])

    # 3. create a new selection for the highlighted residues
    cmd.select("highlighted_residues_1", selection)

    # 4. set the sticks representation for the highlighted residues
    cmd.show("sticks", "highlighted_residues_1")
    util.color_objs("highlighted_residues_1")
    cmd.select('none')
    # cmd.label('''byca(highlighted_residues_1)''', 'oneletter+resi')
    # cmd.set("label_color", "red", 'highlighted_residues_1', quiet=0)  


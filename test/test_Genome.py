import os.path
from genbankqc import Genome


def test_init(genome):
    from genbankqc import Genome
    expected_name = ("GCA_000521565.1_Buchnera_aphidicola_G002_"
                     "Myzus_persicae_Complete_Genome")
    expected_path = os.path.join(genome.species_dir, expected_name+".fasta")
    assert genome.path == expected_path
    assert isinstance(genome, Genome)
    assert genome.name == expected_name
    assert genome.name in genome.msh
    assert genome.path and 'qc' in genome.qc_dir
    assert os.path.isdir(genome.qc_dir)


def test_get_contigs(genome):
    from Bio.Seq import Seq
    assert type(genome.contigs) is list
    assert type(genome.contigs[0]) is Seq
    assert isinstance(genome.count_contigs, int)


def test_assembly_size(genome):
    assert type(genome.assembly_size) is int


def test_unknowns(genome):
    assert type(genome.unknowns) is int


def test_get_distance(aphidicola, genome):
    genome.get_distance(aphidicola.dmx.mean())
    assert isinstance(genome.distance, float)


def test_sketch(genome):
    genome.sketch()
    assert os.path.isfile(genome.msh)


def test_get_stats(genome, aphidicola):
    from pandas import DataFrame
    dmx_mean = aphidicola.dmx.mean()
    genome.get_stats(dmx_mean)
    assert isinstance(genome.stats, DataFrame)
    assert os.path.isfile(genome.stats_path)


def test_parse_biosample(aphidicola, metadata):
    from collections import defaultdict
    for genome in aphidicola.genomes():
        if genome.name == "this_is_a_genome":
            continue
        genome = Genome(genome.path,
                        assembly_summary=metadata.assembly_summary)
        genome.get_biosample()
        assert os.path.isfile(genome.biosample_xml)
        genome.parse_biosample()
        assert isinstance(genome.metadata, defaultdict)

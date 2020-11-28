
process MULTIQC {
    publishDir "${params.output_dir}/multiqc", mode: 'copy'

    input:
    path('fastp/*.json')
    path('prokka/*')

    output:
    file('multiqc_report.html')

    script:

    """
    multiqc . --filename multiqc_report.html
    """
}

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(
        filename,
        df,
        stats
):

    doc = SimpleDocTemplate(
        filename
    )


    styles = getSampleStyleSheet()

    content = []


    title = Paragraph(
        "Traffic Accident Hotspot Analysis Report",
        styles["Title"]
    )

    content.append(title)

    content.append(
        Spacer(1,20)
    )


    total = len(df)

    fatal = len(
        df[df["severity"]=="Fatal"]
    )

    major = len(
        df[df["severity"]=="Major"]
    )

    minor = len(
        df[df["severity"]=="Minor"]
    )

    casualties = df["casualties"].sum()


    report_text = f"""
    <b>Dataset Summary</b><br/><br/>

    Total Accidents:
    {total}<br/>

    Fatal Accidents:
    {fatal}<br/>

    Major Accidents:
    {major}<br/>

    Minor Accidents:
    {minor}<br/>

    Total Casualties:
    {casualties}<br/><br/>


    <b>Highest Risk Hotspot</b><br/><br/>

    Cluster:
    {stats.iloc[0]['cluster']}<br/>

    Accidents:
    {stats.iloc[0]['Accidents']}<br/>

    """


    content.append(
        Paragraph(
            report_text,
            styles["BodyText"]
        )
    )


    doc.build(content)
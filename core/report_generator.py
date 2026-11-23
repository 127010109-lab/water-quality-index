"""
PDF Water Quality Assessment Report Generator using ReportLab.
Produces formal, computer-generated hydrochemical assessment reports containing:
  - Sample identification & report metadata
  - Composite WQI verdicts (WAWQI, CCME WQI, LSI Corrosivity)
  - Detailed analytical parameter breakdown table with compliance flags
  - Targeted engineering remediation prescriptions and multi-barrier treatment plan
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)


class WaterReportGenerator:
    """Compiles computer-generated PDF water quality assessment reports (not accredited laboratory certificates)."""

    def __init__(self, output_dir=None):
        if output_dir:
            self.output_dir = output_dir
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.output_dir = os.path.join(base_dir, "reports")
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_pdf_report(
        self,
        sample_dict,
        wawqi_res,
        ccme_res,
        hydro_res,
        recom_res,
        sample_id="SAMPLE-001",
        source_name="Municipal Tap Water",
        location="Field Monitoring Site",
        analyst_name="Dr. Analytical Hydrochemist"
    ):
        """
        Builds and saves a computer-generated assessment report as a PDF file.

        Returns:
            str: Absolute path to the generated PDF document.
        """
        filename = f"Water_Quality_Certificate_{sample_id.replace(' ', '_')}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        normal = styles["Normal"]

        # Custom typography styles
        title_style = ParagraphStyle(
            "LabTitle",
            parent=normal,
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#1E3A8A")
        )
        subtitle_style = ParagraphStyle(
            "LabSubTitle",
            parent=normal,
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#475569")
        )
        h2_style = ParagraphStyle(
            "SectionH2",
            parent=normal,
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#0F172A")
        )
        cell_bold = ParagraphStyle(
            "CellBold",
            parent=normal,
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#1E293B")
        )
        cell_text = ParagraphStyle(
            "CellText",
            parent=normal,
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#334155")
        )
        cell_compliant = ParagraphStyle(
            "CellComp",
            parent=normal,
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#059669")
        )
        cell_violation = ParagraphStyle(
            "CellViol",
            parent=normal,
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#DC2626")
        )

        story = []

        # 1. Header Banner
        header_text = [
            [
                Paragraph("<b>AQUASAFE WATER QUALITY ASSESSMENT REPORT</b>", title_style),
                Paragraph("<b>COMPUTER-GENERATED SCREENING REPORT</b><br/>Not an accredited laboratory certificate", subtitle_style)
            ],
            [
                Paragraph("Analytical Hydrochemistry & Environmental Quality Decision Support System", subtitle_style),
                Paragraph("Report ID: <b>RPT-" + sample_id + "</b>", subtitle_style)
            ]
        ]
        header_table = Table(header_text, colWidths=[380, 160])
        header_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(header_table)
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceAfter=10, spaceBefore=4))

        # 2. Sample Metadata Table
        meta_data = [
            [
                Paragraph("<b>Sample ID:</b>", cell_bold), Paragraph(str(sample_id), cell_text),
                Paragraph("<b>Date of Analysis:</b>", cell_bold), Paragraph("November 2026", cell_text)
            ],
            [
                Paragraph("<b>Water Source:</b>", cell_bold), Paragraph(str(source_name), cell_text),
                Paragraph("<b>Sampling Location:</b>", cell_bold), Paragraph(str(location), cell_text)
            ],
            [
                Paragraph("<b>Lead Analyst:</b>", cell_bold), Paragraph(str(analyst_name), cell_text),
                Paragraph("<b>Compliance Standard:</b>", cell_bold), Paragraph("BIS IS 10500:2012 & WHO", cell_text)
            ]
        ]
        meta_table = Table(meta_data, colWidths=[80, 190, 110, 160])
        meta_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 10))

        # 3. Overall Verdict & Composite Index Summary Banner
        wawqi_score = wawqi_res.get("score", 0.0)
        wawqi_grade = wawqi_res.get("grade", "")
        wawqi_status = wawqi_res.get("status", "")
        ccme_score = ccme_res.get("score", 0.0)
        ccme_status = ccme_res.get("status", "")
        lsi_val = hydro_res.get("lsi", 0.0)
        lsi_status = hydro_res.get("lsi_status", "")
        potability_verdict = recom_res.get("verdict", "")

        # Screening caution: no limit exceeded does not guarantee good overall quality.
        _poor_grade = any(g in str(wawqi_grade) for g in ("C", "D", "E"))
        _is_potable = "Potable" in potability_verdict and "Non" not in potability_verdict
        if _is_potable and _poor_grade:
            potability_verdict = "All guideline limits met, but the WAWQI grade is poor - further assessment advised"
            banner_bg = colors.HexColor("#FFFBEB")
            banner_border = colors.HexColor("#F59E0B")
            banner_text_color = colors.HexColor("#92400E")
        elif _is_potable:
            banner_bg = colors.HexColor("#ECFDF5")
            banner_border = colors.HexColor("#10B981")
            banner_text_color = colors.HexColor("#065F46")
        else:
            banner_bg = colors.HexColor("#FEF2F2")
            banner_border = colors.HexColor("#EF4444")
            banner_text_color = colors.HexColor("#991B1B")

        banner_data = [
            [
                Paragraph(f"<b>SCREENING RESULT: {potability_verdict.upper()}</b>", ParagraphStyle(
                    "VerdictBanner", parent=normal, fontName="Helvetica-Bold", fontSize=11, textColor=banner_text_color
                ))
            ],
            [
                Paragraph(
                    f"<b>WAWQI Score:</b> {wawqi_score} ({wawqi_grade} - {wawqi_status}) &nbsp;|&nbsp; "
                    f"<b>CCME Index:</b> {ccme_score} ({ccme_status}) &nbsp;|&nbsp; "
                    f"<b>LSI Corrosivity:</b> {lsi_val} ({lsi_status})",
                    cell_text
                )
            ]
        ]
        banner_table = Table(banner_data, colWidths=[540])
        banner_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), banner_bg),
            ("BOX", (0, 0), (-1, -1), 1.0, banner_border),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(banner_table)
        story.append(Spacer(1, 10))

        # 4. Physicochemical Analytical Breakdown Table
        story.append(Paragraph("<b>Analytical Physicochemical Parameter Breakdown</b>", h2_style))
        story.append(Spacer(1, 4))

        param_headers = [
            Paragraph("<b>Parameter</b>", cell_bold),
            Paragraph("<b>Measured</b>", cell_bold),
            Paragraph("<b>Unit</b>", cell_bold),
            Paragraph("<b>Permissible Limit (Si)</b>", cell_bold),
            Paragraph("<b>Unit Weight (Wi)</b>", cell_bold),
            Paragraph("<b>Sub-Index (qi)</b>", cell_bold),
            Paragraph("<b>Compliance</b>", cell_bold)
        ]
        table_rows = [param_headers]

        violations_keys = {v["parameter"]: v for v in wawqi_res.get("violations", [])}

        for param, s_info in wawqi_res.get("sub_indices", {}).items():
            is_breach = param in violations_keys
            status_p = Paragraph("VIOLATION", cell_violation) if is_breach else Paragraph("COMPLIANT", cell_compliant)
            
            # Format display unit cleanly without raw unicode issues
            clean_unit = s_info.get("unit", "").replace("µ", "u")

            table_rows.append([
                Paragraph(s_info.get("name", param), cell_text),
                Paragraph(str(s_info.get("value", "")), cell_text),
                Paragraph(clean_unit, cell_text),
                Paragraph(f"<= {s_info.get('standard', '')}", cell_text),
                Paragraph(str(s_info.get("wi", "")), cell_text),
                Paragraph(str(s_info.get("qi", "")), cell_text),
                status_p
            ])

        param_table = Table(table_rows, colWidths=[130, 55, 55, 100, 65, 65, 70])
        param_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(param_table)
        story.append(Spacer(1, 10))

        # 5. Prescribed Engineering Remediation Solutions
        story.append(Paragraph("<b>Prescribed Engineering Remediation & Water Purification Plan</b>", h2_style))
        story.append(Spacer(1, 4))

        action_items = recom_res.get("action_items", [])
        if not action_items:
            rem_rows = [
                [Paragraph("<b>Status:</b> No chemical remediation required. Water complies with drinking guidelines.", cell_compliant)]
            ]
            rem_table = Table(rem_rows, colWidths=[540])
            rem_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ECFDF5")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#10B981")),
                ("PADDING", (0, 0), (-1, -1), 6)
            ]))
            story.append(rem_table)
        else:
            rem_headers = [
                Paragraph("<b>Identified Contaminant</b>", cell_bold),
                Paragraph("<b>Engineering Technology</b>", cell_bold),
                Paragraph("<b>Scientific Mechanism & Target</b>", cell_bold),
                Paragraph("<b>Household Solution</b>", cell_bold)
            ]
            rem_rows = [rem_headers]
            for act in action_items:
                rem_rows.append([
                    Paragraph(f"<b>{act.get('parameter', '')}</b><br/>({act.get('urgency', '')})", cell_text),
                    Paragraph(act.get("technology", ""), cell_bold),
                    Paragraph(act.get("scientific_mechanism", ""), cell_text),
                    Paragraph(act.get("household_solution", ""), cell_text)
                ])
            rem_table = Table(rem_rows, colWidths=[100, 120, 180, 140])
            rem_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#334155")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FFFBEB")]),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(rem_table)

        story.append(Spacer(1, 14))

        # 6. Formal Sign-off Section
        sign_data = [
            [
                Paragraph("<b>Prepared By:</b><br/><br/>___________________________<br/><b>Name / Signature / Date</b><br/>(Optional - for course or internal use)", cell_text),
                Paragraph("<b>Reviewed By:</b><br/><br/>___________________________<br/><b>Reviewer / Supervisor</b><br/>(Optional)", cell_text)
            ]
        ]
        sign_table = Table(sign_data, colWidths=[270, 270])
        sign_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(KeepTogether(sign_table))
        story.append(Spacer(1, 10))
        story.append(Paragraph("<i>Disclaimer: This report was produced by the AquaSafe software from the values entered by the user. It is a screening-level assessment using standard index equations and published guideline limits. It is not an accredited laboratory certificate and must not be used as a legal or public-health determination of potability. Confirm any result with measurements from an accredited laboratory.</i>", cell_text))

        # Build PDF
        doc.build(story)
        return filepath

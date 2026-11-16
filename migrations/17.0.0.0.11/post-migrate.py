"""Move seeded sequences past the numbers already issued.

Up to 17.0.0.0.10, data/ir.sequence.csv carried number_next, and Odoo reloads CSV data on every
module update, so each update set these sequences back to their Clear-DB start numbers and the
next documents reused numbers already issued (sale orders S01665... created again). The start
numbers are now install-only (data/ir_sequence_start_numbers.xml). This repairs databases that
were updated before: for each of those sequences whose code is also a model name (sale.order,
purchase.order, ...), the next number is raised above the highest number already used by that
company's records. It is never lowered. Sequences of other codes are listed in the log.
"""

import logging
import re

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

SEQUENCES = [
    "ir_sequence_purchase_order_14",
    "ir_sequence_pr_sequence_no",
    "ir_sequence_unbuild_1376",
    "ir_sequence_pr_non_invt_sequence_no_885",
    "ir_sequence_cpr_sequence_no_886",
    "ir_sequence_con_consolidated_sequence_no_887",
    "ir_sequence_consignment_sequence_no_888",
    "ir_sequence_cc_sequence_no_889",
    "ir_sequence_ot_sequence_no_893",
    "ir_sequence_npo_sequence_no_894",
    "ir_sequence_purchase_order",
    "ir_sequence_sales_order",
    "ir_sequence_pr_sequence_no_898",
    "ir_sequence_tp_invoice_no_899",
    "ir_sequence_material_request",
    "ir_sequence_purchase_request",
    "ir_sequence_ot_sheet_sequence",
]


def migrate(cr, version):
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    for xmlid in SEQUENCES:
        seq = env.ref(f"Jinasena_MasterData_Common.{xmlid}", raise_if_not_found=False)
        if not seq or seq.implementation != "standard" or seq.use_date_range:
            continue
        model = env.get(seq.code)
        if model is None or "name" not in model._fields or not model._fields["name"].store:
            _logger.info(
                "[Jinasena_MasterData_Common] %s (%s): no model of that name, not checked",
                xmlid,
                seq.code,
            )
            continue
        prefix, suffix = seq.with_company(seq.company_id)._get_prefix_suffix()
        domain = [("name", "=like", prefix.replace("%", r"\%").replace("_", r"\_") + "%")]
        if seq.company_id and "company_id" in model._fields:
            domain.append(("company_id", "=", seq.company_id.id))
        pattern = re.compile(re.escape(prefix) + r"(\d+)" + re.escape(suffix or "") + "$")
        names = model.sudo().with_context(active_test=False).search(domain).mapped("name")
        used = [int(m.group(1)) for name in names if (m := pattern.match(name or ""))]
        if used and max(used) >= seq.number_next_actual:
            _logger.info(
                "[Jinasena_MasterData_Common] %s: next number %s -> %s (highest used %s%s)",
                xmlid,
                seq.number_next_actual,
                max(used) + 1,
                prefix,
                max(used),
            )
            seq.write({"number_next": max(used) + 1})

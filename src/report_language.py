# -*- coding: utf-8 -*-
"""Helpers for report output language selection and localization."""

from __future__ import annotations

import os
import re
from typing import Any, Dict, Optional

SUPPORTED_REPORT_LANGUAGES = ("zh", "en")

_REPORT_LANGUAGE_ALIASES = {
    "zh-cn": "zh",
    "zh_cn": "zh",
    "zh-hans": "zh",
    "zh_hans": "zh",
    "zh-tw": "zh",
    "zh_tw": "zh",
    "cn": "zh",
    "chinese": "zh",
    "english": "en",
    "en-us": "en",
    "en_us": "en",
    "en-gb": "en",
    "en_gb": "en",
}

_OPERATION_ADVICE_CANONICAL_MAP = {
    "强烈买入": "strong_buy",
    "strong buy": "strong_buy",
    "strong_buy": "strong_buy",
    "买入": "buy",
    "buy": "buy",
    "加仓": "buy",
    "accumulate": "buy",
    "add position": "buy",
    "持有": "hold",
    "洗盘观察": "hold",
    "观察": "hold",
    "hold": "hold",
    "观望": "watch",
    "watch": "watch",
    "wait": "watch",
    "wait and see": "watch",
    "减仓": "reduce",
    "reduce": "reduce",
    "trim": "reduce",
    "卖出": "sell",
    "sell": "sell",
    "强烈卖出": "strong_sell",
    "strong sell": "strong_sell",
    "strong_sell": "strong_sell",
}

_OPERATION_ADVICE_TRANSLATIONS = {
    "strong_buy": {"zh": "强烈买入", "en": "Strong Buy"},
    "buy": {"zh": "买入", "en": "Buy"},
    "hold": {"zh": "持有", "en": "Hold"},
    "watch": {"zh": "观望", "en": "Watch"},
    "reduce": {"zh": "减仓", "en": "Reduce"},
    "sell": {"zh": "卖出", "en": "Sell"},
    "strong_sell": {"zh": "强烈卖出", "en": "Strong Sell"},
}

_TREND_PREDICTION_CANONICAL_MAP = {
    "强势空头": "strong_bearish",
    "强烈看多": "strong_bullish",
    "strong bullish": "strong_bullish",
    "very bullish": "strong_bullish",
    "强势多头": "strong_bullish",
    "多头排列": "bullish",
    "空头排列": "bearish",
    "弱势多头": "bullish",
    "弱势空头": "bearish",
    "看多": "bullish",
    "盘整": "sideways",
    "bullish": "bullish",
    "uptrend": "bullish",
    "震荡": "sideways",
    "neutral": "sideways",
    "sideways": "sideways",
    "range-bound": "sideways",
    "看空": "bearish",
    "bearish": "bearish",
    "downtrend": "bearish",
    "强烈看空": "strong_bearish",
    "strong bearish": "strong_bearish",
    "very bearish": "strong_bearish",
}

_TREND_PREDICTION_TRANSLATIONS = {
    "strong_bullish": {"zh": "强烈看多", "en": "Strong Bullish"},
    "bullish": {"zh": "看多", "en": "Bullish"},
    "sideways": {"zh": "震荡", "en": "Sideways"},
    "bearish": {"zh": "看空", "en": "Bearish"},
    "strong_bearish": {"zh": "强烈看空", "en": "Strong Bearish"},
}

_CONFIDENCE_LEVEL_CANONICAL_MAP = {
    "高": "high",
    "high": "high",
    "中": "medium",
    "medium": "medium",
    "med": "medium",
    "低": "low",
    "low": "low",
}

_CONFIDENCE_LEVEL_TRANSLATIONS = {
    "high": {"zh": "高", "en": "High"},
    "medium": {"zh": "中", "en": "Medium"},
    "low": {"zh": "低", "en": "Low"},
}

_CHIP_HEALTH_CANONICAL_MAP = {
    "健康": "healthy",
    "healthy": "healthy",
    "一般": "average",
    "average": "average",
    "警惕": "caution",
    "caution": "caution",
}

_CHIP_HEALTH_TRANSLATIONS = {
    "healthy": {"zh": "健康", "en": "Healthy"},
    "average": {"zh": "一般", "en": "Average"},
    "caution": {"zh": "警惕", "en": "Caution"},
}

_BIAS_STATUS_CANONICAL_MAP = {
    "安全": "safe",
    "safe": "safe",
    "警戒": "caution",
    "警惕": "caution",
    "caution": "caution",
    "危险": "danger",
    "risk": "danger",
    "danger": "danger",
}

_BIAS_STATUS_TRANSLATIONS = {
    "safe": {"zh": "安全", "en": "Safe"},
    "caution": {"zh": "警戒", "en": "Caution"},
    "danger": {"zh": "危险", "en": "Danger"},
}

_PLACEHOLDER_BY_LANGUAGE = {
    "zh": "待补充",
    "en": "TBD",
}

_UNKNOWN_BY_LANGUAGE = {
    "zh": "未知",
    "en": "Unknown",
}

_NO_DATA_BY_LANGUAGE = {
    "zh": "数据缺失",
    "en": "Data unavailable",
}

_CHIP_UNAVAILABLE_BY_LANGUAGE = {
    "zh": "筹码分布未启用或数据源暂不可用，未纳入筹码判断。",
    "en": "Chip distribution is disabled or temporarily unavailable; chip signals were not used.",
}

_CHIP_PLACEHOLDER_EXACT = {
    "",
    "n/a",
    "na",
    "none",
    "null",
    "unknown",
    "tbd",
    "数据缺失",
    "未知",
    "暂无",
    "待补充",
}

_CHIP_PLACEHOLDER_HINTS = (
    "数据缺失",
    "无法判断",
    "data unavailable",
    "unavailable",
    "not available",
    "missing",
    "not supported",
)

_CHIP_METRIC_KEYS = ("profit_ratio", "avg_cost", "concentration")
_CHIP_UNAVAILABLE_REASON_KEYS = (
    "chip_unavailable_reason",
    "unavailable_reason",
    "chip_unavailable",
)

_GENERIC_STOCK_NAME_BY_LANGUAGE = {
    "zh": "待确认股票",
    "en": "Unnamed Stock",
}

_REPORT_LABELS: Dict[str, Dict[str, str]] = {
    "zh": {
        "dashboard_title": "决策仪表盘",
        "brief_title": "决策简报",
        "analyzed_prefix": "共分析",
        "stock_unit": "只股票",
        "stock_unit_compact": "只",
        "buy_label": "买入",
        "watch_label": "观望",
        "sell_label": "卖出",
        "summary_heading": "分析结果摘要",
        "info_heading": "重要信息速览",
        "sentiment_summary_label": "舆情情绪",
        "earnings_outlook_label": "业绩预期",
        "risk_alerts_label": "风险警报",
        "positive_catalysts_label": "利好催化",
        "latest_news_label": "最新动态",
        "core_conclusion_heading": "核心结论",
        "one_sentence_label": "一句话决策",
        "time_sensitivity_label": "时效性",
        "default_time_sensitivity": "本周内",
        "position_status_label": "持仓情况",
        "action_advice_label": "操作建议",
        "no_position_label": "空仓者",
        "has_position_label": "持仓者",
        "continue_holding": "继续持有",
        "market_snapshot_heading": "当日行情",
        "close_label": "收盘",
        "prev_close_label": "昨收",
        "open_label": "开盘",
        "high_label": "最高",
        "low_label": "最低",
        "change_pct_label": "涨跌幅",
        "change_amount_label": "涨跌额",
        "amplitude_label": "振幅",
        "volume_label": "成交量",
        "amount_label": "成交额",
        "current_price_label": "当前价",
        "volume_ratio_label": "量比",
        "turnover_rate_label": "换手率",
        "source_label": "行情来源",
        "data_perspective_heading": "数据透视",
        "ma_alignment_label": "均线排列",
        "bullish_alignment_label": "多头排列",
        "yes_label": "是",
        "no_label": "否",
        "trend_strength_label": "趋势强度",
        "price_metrics_label": "价格指标",
        "ma5_label": "MA5",
        "ma10_label": "MA10",
        "ma20_label": "MA20",
        "bias_ma5_label": "乖离率(MA5)",
        "support_level_label": "支撑位",
        "resistance_level_label": "压力位",
        "chip_label": "筹码",
        "phase_decision_heading": "盘中决策护栏",
        "action_window_label": "行动窗口",
        "immediate_action_label": "当前动作",
        "watch_conditions_label": "观察条件",
        "next_check_time_label": "下次检查",
        "confidence_reason_label": "置信度理由",
        "data_limitations_label": "数据限制",
        "battle_plan_heading": "作战计划",
        "ideal_buy_label": "理想买入点",
        "secondary_buy_label": "次优买入点",
        "stop_loss_label": "止损位",
        "take_profit_label": "目标位",
        "suggested_position_label": "仓位建议",
        "entry_plan_label": "建仓策略",
        "risk_control_label": "风控策略",
        "checklist_heading": "检查清单",
        "failed_checks_heading": "检查未通过项",
        "history_compare_heading": "历史信号对比",
        "time_label": "时间",
        "score_label": "评分",
        "advice_label": "建议",
        "trend_label": "趋势",
        "generated_at_label": "报告生成时间",
        "report_time_label": "生成时间",
        "no_results": "无分析结果",
        "report_title": "股票分析报告",
        "avg_score_label": "均分",
        "action_points_heading": "操作点位",
        "position_advice_heading": "持仓建议",
        "analysis_model_label": "分析模型",
        "not_investment_advice": "AI生成，仅供参考，不构成投资建议",
        "details_report_hint": "详细报告见",
        "financial_summary_heading": "财务摘要",
        "report_date_label": "报告期",
        "revenue_label": "营业收入",
        "net_profit_label": "归母净利润",
        "operating_cash_flow_label": "经营现金流",
        "roe_label": "ROE",
        "revenue_yoy_label": "营收同比",
        "net_profit_yoy_label": "净利同比",
        "gross_margin_label": "毛利率",
        "shareholder_return_heading": "股东回报",
        "ttm_cash_dividend_label": "近12月每股现金分红(税前)",
        "ttm_event_count_label": "近12月分红次数",
        "ttm_dividend_yield_label": "TTM 股息率",
        "latest_ex_dividend_label": "最近除息日",
        "related_boards_heading": "关联板块",
        "industry_boards_heading": "行业板块",
        "concept_boards_heading": "概念板块",
        "board_name_label": "板块",
        "board_type_label": "类型",
        "board_status_label": "板块表现",
        "board_change_pct_label": "板块涨跌幅",
        "leading_board_label": "领涨",
        "lagging_board_label": "领跌",
        "signal_attribution_heading": "信号归因分析",
        "attribution_weights_label": "归因权重",
        "technical_indicators_label": "技术指标",
        "news_sentiment_label": "新闻舆情",
        "fundamentals_label": "基本面",
        "market_conditions_label": "市场环境",
        "strongest_bullish_signal_label": "最强看多信号",
        "strongest_bearish_signal_label": "最强看空信号",
    },
    "en": {
        "dashboard_title": "Decision Dashboard",
        "brief_title": "Decision Brief",
        "analyzed_prefix": "Analyzed",
        "stock_unit": "stocks",
        "stock_unit_compact": "stocks",
        "buy_label": "Buy",
        "watch_label": "Watch",
        "sell_label": "Sell",
        "summary_heading": "Summary",
        "info_heading": "Key Updates",
        "sentiment_summary_label": "Sentiment",
        "earnings_outlook_label": "Earnings Outlook",
        "risk_alerts_label": "Risk Alerts",
        "positive_catalysts_label": "Positive Catalysts",
        "latest_news_label": "Latest News",
        "core_conclusion_heading": "Core Conclusion",
        "one_sentence_label": "One-line Decision",
        "time_sensitivity_label": "Time Sensitivity",
        "default_time_sensitivity": "This week",
        "position_status_label": "Position",
        "action_advice_label": "Action",
        "no_position_label": "No Position",
        "has_position_label": "Holding",
        "continue_holding": "Continue holding",
        "market_snapshot_heading": "Market Snapshot",
        "close_label": "Close",
        "prev_close_label": "Prev Close",
        "open_label": "Open",
        "high_label": "High",
        "low_label": "Low",
        "change_pct_label": "Change %",
        "change_amount_label": "Change",
        "amplitude_label": "Amplitude",
        "volume_label": "Volume",
        "amount_label": "Turnover",
        "current_price_label": "Price",
        "volume_ratio_label": "Volume Ratio",
        "turnover_rate_label": "Turnover Rate",
        "source_label": "Source",
        "data_perspective_heading": "Data View",
        "ma_alignment_label": "MA Alignment",
        "bullish_alignment_label": "Bullish Alignment",
        "yes_label": "Yes",
        "no_label": "No",
        "trend_strength_label": "Trend Strength",
        "price_metrics_label": "Price Metrics",
        "ma5_label": "MA5",
        "ma10_label": "MA10",
        "ma20_label": "MA20",
        "bias_ma5_label": "Bias (MA5)",
        "support_level_label": "Support",
        "resistance_level_label": "Resistance",
        "chip_label": "Chip Structure",
        "phase_decision_heading": "Phase Decision Guardrail",
        "action_window_label": "Action Window",
        "immediate_action_label": "Current Action",
        "watch_conditions_label": "Watch Conditions",
        "next_check_time_label": "Next Check",
        "confidence_reason_label": "Confidence Reason",
        "data_limitations_label": "Data Limitations",
        "battle_plan_heading": "Battle Plan",
        "ideal_buy_label": "Ideal Entry",
        "secondary_buy_label": "Secondary Entry",
        "stop_loss_label": "Stop Loss",
        "take_profit_label": "Target",
        "suggested_position_label": "Position Size",
        "entry_plan_label": "Entry Plan",
        "risk_control_label": "Risk Control",
        "checklist_heading": "Checklist",
        "failed_checks_heading": "Failed Checks",
        "history_compare_heading": "Historical Signal Comparison",
        "time_label": "Time",
        "score_label": "Score",
        "advice_label": "Advice",
        "trend_label": "Trend",
        "generated_at_label": "Generated At",
        "report_time_label": "Generated",
        "no_results": "No analysis results",
        "report_title": "Stock Analysis Report",
        "avg_score_label": "Avg Score",
        "action_points_heading": "Action Levels",
        "position_advice_heading": "Position Advice",
        "analysis_model_label": "Model",
        "not_investment_advice": "AI-generated content for reference only. Not investment advice.",
        "details_report_hint": "See detailed report:",
        "financial_summary_heading": "Financial Summary",
        "report_date_label": "Report Date",
        "revenue_label": "Revenue",
        "net_profit_label": "Net Profit (Parent)",
        "operating_cash_flow_label": "Operating Cash Flow",
        "roe_label": "ROE",
        "revenue_yoy_label": "Revenue YoY",
        "net_profit_yoy_label": "Net Profit YoY",
        "gross_margin_label": "Gross Margin",
        "shareholder_return_heading": "Shareholder Return",
        "ttm_cash_dividend_label": "TTM Cash Dividend / Share (Pre-tax)",
        "ttm_event_count_label": "TTM Dividend Events",
        "ttm_dividend_yield_label": "TTM Dividend Yield",
        "latest_ex_dividend_label": "Latest Ex-dividend Date",
        "related_boards_heading": "Related Boards",
        "industry_boards_heading": "Industry Sectors",
        "concept_boards_heading": "Concept Themes",
        "board_name_label": "Board",
        "board_type_label": "Type",
        "board_status_label": "Status",
        "board_change_pct_label": "Change %",
        "leading_board_label": "Leading",
        "lagging_board_label": "Lagging",
        "signal_attribution_heading": "Signal Attribution",
        "attribution_weights_label": "Attribution Weights",
        "technical_indicators_label": "Technical Indicators",
        "news_sentiment_label": "News Sentiment",
        "fundamentals_label": "Fundamentals",
        "market_conditions_label": "Market Conditions",
        "strongest_bullish_signal_label": "Strongest Bullish Signal",
        "strongest_bearish_signal_label": "Strongest Bearish Signal",
    },
}

_DECISION_INTENT_NEGATIONS = (
    "不",
    "并非",
    "并未",
    "未",
    "没有",
    "无",
    "不是",
    "no ",
    "not ",
    " never",
)

_DECISION_INTENT_NEGATION_SCOPE_BREAK_CHARS = "，,。；;:!?！？"
_DECISION_INTENT_NEGATION_CONNECTORS = (
    "建议",
    "应",
    "应当",
    "宜",
    "先",
    "再",
    "暂",
    "暂时",
    "可",
    "可以",
    "需要",
    "需",
    "继续",
)


def _strip_decision_negation_connectors(text: str) -> str:
    """Remove common advisory connectors between a negation token and decision word."""
    suffix = text.strip()
    changed = True
    while changed:
        changed = False
        for connector in _DECISION_INTENT_NEGATION_CONNECTORS:
            if suffix.startswith(connector):
                suffix = suffix[len(connector):].strip()
                changed = True
                break
    return suffix


def normalize_report_language(value: Optional[str], default: str = "zh") -> str:
    """Normalize report language to a supported short code."""
    candidate = (value or default).strip().lower().replace(" ", "_")
    candidate = _REPORT_LANGUAGE_ALIASES.get(candidate, candidate)
    if candidate in SUPPORTED_REPORT_LANGUAGES:
        return candidate
    return default


def is_supported_report_language_value(value: Optional[str]) -> bool:
    """Return whether the raw value is a supported language code or alias."""
    candidate = (value or "").strip().lower().replace(" ", "_")
    if not candidate:
        return False
    return candidate in SUPPORTED_REPORT_LANGUAGES or candidate in _REPORT_LANGUAGE_ALIASES


def get_report_labels(language: Optional[str]) -> Dict[str, str]:
    """Return UI copy for the selected report language."""
    normalized = normalize_report_language(language)
    return _REPORT_LABELS[normalized]


def get_placeholder_text(language: Optional[str]) -> str:
    """Return placeholder text for missing localized content."""
    return _PLACEHOLDER_BY_LANGUAGE[normalize_report_language(language)]


def get_unknown_text(language: Optional[str]) -> str:
    """Return localized unknown text."""
    return _UNKNOWN_BY_LANGUAGE[normalize_report_language(language)]


def get_no_data_text(language: Optional[str]) -> str:
    """Return localized data unavailable text."""
    return _NO_DATA_BY_LANGUAGE[normalize_report_language(language)]


def get_chip_unavailable_text(language: Optional[str]) -> str:
    """Return the localized one-line chip distribution fallback text."""
    return _CHIP_UNAVAILABLE_BY_LANGUAGE[normalize_report_language(language)]


def _normalize_lookup_key(value: Any) -> str:
    return str(value or "").strip().lower().replace("_", " ").replace("-", " ")


def _iter_lookup_candidates(value: Any) -> list[str]:
    raw_text = str(value or "").strip()
    if not raw_text:
        return []

    candidates = [raw_text]
    for part in re.split(r"[/|,，、]+", raw_text):
        normalized = part.strip()
        if normalized and normalized not in candidates:
            candidates.append(normalized)
    return candidates


def _canonicalize_lookup_value(value: Any, canonical_map: Dict[str, str]) -> Optional[str]:
    for candidate in _iter_lookup_candidates(value):
        canonical = canonical_map.get(_normalize_lookup_key(candidate))
        if canonical:
            return canonical
    return None


def _first_non_negated_position(text: str, token: str) -> Optional[int]:
    if not text or not token:
        return None

    normalized_text = text.lower().strip()
    if any(ch in normalized_text for ch in "abcdefghijklmnopqrstuvwxyz"):
        matches = list(re.finditer(rf"(?<![a-z0-9_]){re.escape(token)}(?![a-z0-9_])", normalized_text))
    else:
        matches = list(re.finditer(re.escape(token), normalized_text))

    for match in matches:
        prefix = normalized_text[: match.start()]
        if any(prefix.rstrip().endswith(neg) for neg in _DECISION_INTENT_NEGATIONS):
            continue
        lookback = prefix[-12:]
        negated = False
        for neg in _DECISION_INTENT_NEGATIONS:
            if not neg:
                continue
            neg_idx = lookback.rfind(neg)
            if neg_idx < 0:
                continue
            suffix = lookback[neg_idx + len(neg):]
            if not suffix:
                negated = True
                break
            if any(ch in suffix for ch in _DECISION_INTENT_NEGATION_SCOPE_BREAK_CHARS):
                continue
            normalized_suffix = _strip_decision_negation_connectors(suffix)
            if not normalized_suffix:
                negated = True
                break
            if any(ch in normalized_suffix for ch in _DECISION_INTENT_NEGATION_SCOPE_BREAK_CHARS):
                continue
            if len(normalized_suffix) > 6 and token not in normalized_suffix:
                continue
            if normalized_suffix.startswith(token):
                negated = True
                break
        if negated:
            continue
        else:
            return match.start()
    return None


def _is_placeholder_stock_name(value: Any, code: Any = None) -> bool:
    text = str(value or "").strip()
    if not text:
        return True

    lowered = text.lower()
    if lowered in {"n/a", "na", "none", "null", "unknown"}:
        return True
    if text in {"-", "—", "未知", "待补充"}:
        return True

    code_text = str(code or "").strip()
    if code_text and lowered == code_text.lower():
        return True

    return text.startswith("股票")


def _translate_from_map(
    value: Any,
    language: Optional[str],
    *,
    canonical_map: Dict[str, str],
    translations: Dict[str, Dict[str, str]],
) -> str:
    normalized_language = normalize_report_language(language)
    raw_text = str(value or "").strip()
    if not raw_text:
        return raw_text

    canonical = _canonicalize_lookup_value(raw_text, canonical_map)
    if canonical:
        return translations[canonical][normalized_language]
    return raw_text


def localize_operation_advice(value: Any, language: Optional[str]) -> str:
    """Translate operation advice between Chinese and English when recognized."""
    return _translate_from_map(
        value,
        language,
        canonical_map=_OPERATION_ADVICE_CANONICAL_MAP,
        translations=_OPERATION_ADVICE_TRANSLATIONS,
    )


def localize_trend_prediction(value: Any, language: Optional[str]) -> str:
    """Translate trend prediction between Chinese and English when recognized."""
    normalized_language = normalize_report_language(language)
    raw_text = str(value or "").strip()
    if not raw_text:
        return raw_text
    if normalized_language == "zh":
        if re.search(r"[\u4e00-\u9fff]", raw_text):
            return raw_text
    return _translate_from_map(
        value,
        normalized_language,
        canonical_map=_TREND_PREDICTION_CANONICAL_MAP,
        translations=_TREND_PREDICTION_TRANSLATIONS,
    )


def localize_confidence_level(value: Any, language: Optional[str]) -> str:
    """Translate confidence level between Chinese and English when recognized."""
    return _translate_from_map(
        value,
        language,
        canonical_map=_CONFIDENCE_LEVEL_CANONICAL_MAP,
        translations=_CONFIDENCE_LEVEL_TRANSLATIONS,
    )


def localize_chip_health(value: Any, language: Optional[str]) -> str:
    """Translate chip health labels between Chinese and English when recognized."""
    return _translate_from_map(
        value,
        language,
        canonical_map=_CHIP_HEALTH_CANONICAL_MAP,
        translations=_CHIP_HEALTH_TRANSLATIONS,
    )


def is_chip_placeholder_value(value: Any) -> bool:
    """Return True for chip fields filled with empty or no-data placeholders."""
    if value is None:
        return True
    if isinstance(value, (int, float)) and value == 0:
        return True
    text = str(value).strip()
    lowered = text.lower()
    if lowered in _CHIP_PLACEHOLDER_EXACT:
        return True
    return any(hint in lowered for hint in _CHIP_PLACEHOLDER_HINTS)


def is_chip_structure_unavailable(chip_data: Any) -> bool:
    """Detect chip_structure blocks that contain only unavailable placeholders."""
    if not isinstance(chip_data, dict) or not chip_data:
        return False
    for key in _CHIP_UNAVAILABLE_REASON_KEYS:
        raw = chip_data.get(key)
        if isinstance(raw, bool):
            if raw:
                return True
            continue
        if str(raw or "").strip():
            return True
    if any(key in chip_data for key in _CHIP_METRIC_KEYS):
        return all(is_chip_placeholder_value(chip_data.get(key)) for key in _CHIP_METRIC_KEYS)
    return all(is_chip_placeholder_value(value) for value in chip_data.values())


def get_chip_unavailable_reason(value: Any, language: Optional[str]) -> str:
    """Return the explicit or default chip unavailable reason for rendering."""
    if not isinstance(value, dict) or not value:
        return ""
    for key in _CHIP_UNAVAILABLE_REASON_KEYS:
        raw = value.get(key)
        if isinstance(raw, bool):
            if raw:
                return get_chip_unavailable_text(language)
            continue
        text = str(raw or "").strip()
        if text:
            return text
    if is_chip_structure_unavailable(value):
        return get_chip_unavailable_text(language)
    return ""


def localize_bias_status(value: Any, language: Optional[str]) -> str:
    """Translate price bias status labels between Chinese and English when recognized."""
    return _translate_from_map(
        value,
        language,
        canonical_map=_BIAS_STATUS_CANONICAL_MAP,
        translations=_BIAS_STATUS_TRANSLATIONS,
    )


def get_bias_status_emoji(value: Any) -> str:
    """Return the stable alert emoji for a localized or canonical bias status."""
    canonical = _canonicalize_lookup_value(value, _BIAS_STATUS_CANONICAL_MAP)
    if canonical == "safe":
        return "✅"
    if canonical == "caution":
        return "⚠️"
    return "🚨"


def infer_decision_type_from_advice(value: Any, default: str = "hold") -> str:
    """Infer buy/hold/sell from human-readable operation advice."""
    canonical = _canonicalize_lookup_value(value, _OPERATION_ADVICE_CANONICAL_MAP)
    if canonical in {"strong_buy", "buy"}:
        return "buy"
    if canonical in {"reduce", "sell", "strong_sell"}:
        return "sell"
    if canonical in {"hold", "watch"}:
        return "hold"

    normalized_text = _normalize_lookup_key(value)
    best_position: Optional[int] = None
    best_canonical: Optional[str] = None
    for option, canonical in _OPERATION_ADVICE_CANONICAL_MAP.items():
        option_norm = _normalize_lookup_key(option)
        pos = _first_non_negated_position(normalized_text, option_norm)
        if pos is None:
            continue
        if best_position is None or pos < best_position:
            best_position = pos
            best_canonical = canonical

    if best_canonical in {"strong_buy", "buy"}:
        return "buy"
    if best_canonical in {"reduce", "sell", "strong_sell"}:
        return "sell"
    if best_canonical in {"hold", "watch"}:
        return "hold"

    return default


def get_signal_level(advice: Any, score: Any, language: Optional[str]) -> tuple[str, str, str]:
    """Return localized signal text, emoji, and stable color tag."""
    normalized_language = normalize_report_language(language)
    canonical = _canonicalize_lookup_value(advice, _OPERATION_ADVICE_CANONICAL_MAP)
    if canonical == "strong_buy":
        return (_OPERATION_ADVICE_TRANSLATIONS["strong_buy"][normalized_language], "💚", "strong_buy")
    if canonical == "buy":
        return (_OPERATION_ADVICE_TRANSLATIONS["buy"][normalized_language], "🟢", "buy")
    if canonical == "hold":
        return (_OPERATION_ADVICE_TRANSLATIONS["hold"][normalized_language], "🟡", "hold")
    if canonical == "watch":
        return (_OPERATION_ADVICE_TRANSLATIONS["watch"][normalized_language], "⚪", "watch")
    if canonical == "reduce":
        return (_OPERATION_ADVICE_TRANSLATIONS["reduce"][normalized_language], "🟠", "reduce")
    if canonical in {"sell", "strong_sell"}:
        return (_OPERATION_ADVICE_TRANSLATIONS["sell"][normalized_language], "🔴", "sell")

    try:
        numeric_score = int(float(score))
    except (TypeError, ValueError):
        numeric_score = 50

    if numeric_score >= 80:
        return (_OPERATION_ADVICE_TRANSLATIONS["strong_buy"][normalized_language], "💚", "strong_buy")
    if numeric_score >= 65:
        return (_OPERATION_ADVICE_TRANSLATIONS["buy"][normalized_language], "🟢", "buy")
    if numeric_score >= 55:
        return (_OPERATION_ADVICE_TRANSLATIONS["hold"][normalized_language], "🟡", "hold")
    if numeric_score >= 45:
        return (_OPERATION_ADVICE_TRANSLATIONS["watch"][normalized_language], "⚪", "watch")
    if numeric_score >= 35:
        return (_OPERATION_ADVICE_TRANSLATIONS["reduce"][normalized_language], "🟠", "reduce")
    return (_OPERATION_ADVICE_TRANSLATIONS["sell"][normalized_language], "🔴", "sell")


def get_localized_stock_name(value: Any, code: Any, language: Optional[str]) -> str:
    """Return a localized stock name placeholder when the original name is missing."""
    raw_text = str(value or "").strip()
    if not _is_placeholder_stock_name(raw_text, code):
        return raw_text
    return _GENERIC_STOCK_NAME_BY_LANGUAGE[normalize_report_language(language)]


def get_sentiment_label(score: int, language: Optional[str]) -> str:
    """Return localized sentiment label by score band."""
    normalized = normalize_report_language(language)
    if normalized == "en":
        if score >= 80:
            return "Very Bullish"
        if score >= 60:
            return "Bullish"
        if score >= 40:
            return "Neutral"
        if score >= 20:
            return "Bearish"
        return "Very Bearish"

    if score >= 80:
        return "极度乐观"
    if score >= 60:
        return "乐观"
    if score >= 40:
        return "中性"
    if score >= 20:
        return "悲观"
    return "极度悲观"


# ---------------------------------------------------------------------------
# General-purpose i18n for log messages, CLI output, API responses
# ---------------------------------------------------------------------------

_GENERAL_TEXT: Dict[str, Dict[str, str]] = {
    "zh": {
        # ── main.py startup / lifecycle ──
        "app_starting": "正在启动 {}...",
        "app_config_init": "正在初始化配置...",
        "app_fastapi_started": "FastAPI 服务已启动: {}",
        "app_not_run_immediately": "配置为不立即运行分析 (RUN_IMMEDIATELY=false)",
        "app_execution_complete": "程序执行完成",
        "app_api_running": "API 服务运行中 (按 Ctrl+C 退出)...",
        "app_worker_running": "分析工作器运行中 (按 Ctrl+C 退出)...",
        "app_worker_starting": "正在启动后台分析工作器...",
        "app_worker_started": "后台分析工作器已启动",
        "app_api_listening": "API 服务监听: {}",
        "app_worker_stopped": "后台分析工作器已停止",
        "app_shutting_down": "正在关闭...",
        "app_shutdown_complete": "关闭完成",
        "app_error_detail": "错误详情: {}",
        "app_fatal_error": "发生致命错误: {}",
        "app_frontend_ready": "前端构建就绪",
        "app_frontend_not_ready": "前端静态资源未就绪，继续启动 FastAPI 服务（Web 页面可能不可用）",
        "app_frontend_build_failed": "前端命令执行失败（exit_code={exit_code}）: {cmd}",
        "app_frontend_building": "正在构建前端资源...",
        "app_scheduler_thread": "定时任务线程",
        "app_analysis_complete": "{} 分析已完成",
        "app_analysis_failed": "{} 分析失败",

        # ── Log prefixes / common ──
        "log_prefix_info": "信息",
        "log_prefix_warn": "警告",
        "log_prefix_error": "错误",
        "log_prefix_debug": "调试",

        # ── API common ──
        "api_internal_error": "内部服务器错误",
        "api_not_found": "未找到",
        "api_bad_request": "请求参数无效",
        "api_unauthorized": "未授权",
        "api_forbidden": "禁止访问",
        "api_too_many_requests": "请求过于频繁",

        # ── Notification ──
        "notif_channel_wechat": "企业微信",
        "notif_channel_feishu": "飞书",
        "notif_channel_telegram": "Telegram",
        "notif_channel_email": "邮件",
        "notif_channel_slack": "Slack",
        "notif_send_success": "通知发送成功 ({channel})",
        "notif_send_failure": "通知发送失败 ({channel}): {detail}",
        "notif_channel_disabled": "通知渠道已禁用: {channel}",

        # ── Analysis / market ──
        "analysis_submitted": "已提交 {symbol} 分析任务：{task_id}",
        "analysis_task_queued": "分析任务已加入队列: {task_id}",
        "analysis_task_running": "正在分析: {symbol}",
        "analysis_task_complete": "分析完成: {symbol}",
        "analysis_task_failed": "分析失败: {symbol} - {detail}",
        "analysis_no_results": "无分析结果",
        "market_morning_greeting": "早上好",
        "market_afternoon_greeting": "下午好",
        "market_evening_greeting": "晚上好",
        "market_session_morning": "早盘",
        "market_session_afternoon": "午盘",
        "market_session_closed": "已收盘",
        "market_session_pre": "盘前",
        "market_session_post": "盘后",
        "market_closed_today": "今日休市",
        "market_open_today": "今日开市",

        # ── Scheduler ──
        "scheduler_starting": "正在启动定时任务调度器...",
        "scheduler_started": "定时任务调度器已启动",
        "scheduler_stopped": "定时任务调度器已停止",
        "scheduler_next_run": "下次执行: {time}",
        "scheduler_skip_holiday": "今日休市，跳过定时任务",
        "scheduler_task_start": "开始执行定时任务: {name}",
        "scheduler_task_done": "定时任务完成: {name}",
        "scheduler_task_failed": "定时任务失败: {name} - {detail}",

        # ── Data provider ──
        "data_fetch_start": "正在从 {source} 获取 {symbol} 数据...",
        "data_fetch_done": "{source} 数据获取完成: {symbol} ({count} 条)",
        "data_fetch_failed": "数据获取失败 ({source}): {detail}",
        "data_fetch_empty": "{source} 未返回 {symbol} 数据",
        "data_fetch_rate_limited": "{source} 请求被限流，等待 {seconds}s 后重试",
        "data_source_fallback": "{source} 不可用，回退到 {fallback}",
        "data_cache_hit": "命中缓存: {key}",
        "data_cache_miss": "缓存未命中: {key}",

        # ── main.py lifecycle ──
        "app_bootstrap_log_failed": "Bootstrap 日志初始化失败，已回退到 stderr: {}",
        "app_config_load_failed": "加载配置失败: {}",
        "app_log_switch_failed": "切换到配置日志目录失败: {}",
        "app_system_start": "A股自选股智能分析系统 启动",
        "app_runtime": "运行时间: {}",
        "app_market_review_running": "大盘复盘正在执行中，跳过本次大盘复盘",
        "app_stock_index_refreshed": "[stock-index] 分析前已刷新股票索引缓存: {}",
        "app_stock_index_incomplete": "[stock-index] 分析前刷新未完成，继续使用本地索引: {}",
        "app_stock_index_failed": "[stock-index] 分析前刷新股票索引失败，继续执行分析: {}",
        "app_all_markets_holiday": "今日所有相关市场均为非交易日，跳过执行。可使用 --force-run 强制执行。",
        "app_holiday_skipped": "今日休市股票已跳过: {}",
        "app_context_reuse_skip": "复盘上下文可复用，跳过重复大盘复盘并复用上下文内容。",
        "app_context_reuse_push_ok": "复用本轮大盘上下文推送大盘复盘成功",
        "app_context_reuse_push_fail": "复用本轮大盘上下文推送大盘复盘失败",
        "app_waiting_market_review": "等待 {} 秒后执行大盘复盘（避免API限流）...",
        "app_combined_push_ok": "已合并推送（个股+大盘复盘）",
        "app_combined_push_fail": "合并推送失败",
        "app_summary_header": "===== 分析结果摘要 =====",
        "app_execution_done": "任务执行完成",
        "app_creating_feishu_doc": "正在创建飞书云文档...",
        "app_feishu_doc_created": "飞书云文档创建成功: {}",
        "app_feishu_doc_failed": "飞书文档生成失败: {}",
        "app_feishu_doc_notify": "[{}] 复盘文档创建成功: {}",
        "app_auto_backtest_start": "开始自动回测...",
        "app_auto_backtest_done": "自动回测完成: processed={processed} saved={saved} failed={failed}",
        "app_auto_backtest_failed": "自动回测失败（已忽略）: {}",
        "app_analysis_flow_failed": "分析流程执行失败: {}",
        "app_fastapi_exited": "FastAPI 服务器启动后立即退出: {}",
        "app_fastapi_timeout": "FastAPI 服务在 {}s 内未完成启动: {}",
        "app_schedule_stocks_param": "定时模式下检测到 --stocks 参数；计划执行将忽略启动时股票快照，并在每次运行前重新读取最新的 STOCK_LIST。",
        "app_cli_stock_list": "使用命令行指定的股票列表: {}",
        "app_config_loading": "正在加载配置...",
        "app_config_validating": "正在验证配置...",
        "app_market_review_reuse_fail": "复用大盘上下文保存大盘复盘报告失败: {}",
        "app_score_format": "评分 {score} | {trend}",
        "app_web_not_started": "Web 界面未启动（使用 --serve 参数启用）",
        "app_feishu_lock": "飞书文档生成功能未启用或加锁失败，跳过",
        "app_config_file_fail": "读取配置文件 {} 失败，继续沿用当前环境变量: {}",
        "app_log_init_fail": "文件日志初始化失败，已降级为控制台日志输出；日志目录 {dir!r} 当前不可写或不可创建: {exc}。官方 Docker 镜像启动入口会自动修复默认挂载目录权限；若仍失败，请检查是否使用了 --user、只读挂载、rootless Docker 或 NFS 等限制写入的环境。",
        "app_user_interrupt": "用户中断，程序退出",
        "app_program_failed": "程序执行失败: {}",
        "app_web_startup_failed": "启动 FastAPI 服务失败: {}",
        "app_web_running": "Web 服务运行中: {}",
        "app_api_trigger": "通过 /api/v1/analysis/analyze 接口触发分析",
        "app_api_docs": "API 文档: {}",
        "app_ctrl_c_exit": "按 Ctrl+C 退出...",
        "app_mode_web_only": "模式: 仅 Web 服务",
        "app_mode_backtest": "模式: 回测",
        "app_mode_market_review_only": "模式: 仅大盘复盘",
        "app_mode_web_api_scheduler": "模式: Web/API runtime scheduler",
        "app_mode_schedule": "模式: 定时任务",
        "app_market_review_holiday": "今日大盘复盘相关市场均为非交易日，跳过执行。可使用 --force-run 强制执行。",
        "app_scheduler_takeover": "Web/API runtime scheduler 已接管定时任务，保存设置会作用于当前进程",
        "app_daily_exec_time": "每日执行时间: {}",
        "app_run_immediately": "启动时立即执行: {}",
        "app_event_monitor": "[EventMonitor] 本轮触发 {} 条提醒",
        "app_context_reuse_msg": "复盘上下文可复用，跳过重复大盘复盘并复用上下文内容。",
        "app_waiting_review": "等待 {} 秒后执行大盘复盘（避免API限流）...",
    },
    "en": {
        "app_starting": "Starting {}...",
        "app_config_init": "Initializing configuration...",
        "app_fastapi_started": "FastAPI server started: {}",
        "app_not_run_immediately": "Configured not to run analysis immediately (RUN_IMMEDIATELY=false)",
        "app_execution_complete": "Execution complete",
        "app_api_running": "API server running (press Ctrl+C to exit)...",
        "app_worker_running": "Analysis worker running (press Ctrl+C to exit)...",
        "app_worker_starting": "Starting background analysis worker...",
        "app_worker_started": "Background analysis worker started",
        "app_api_listening": "API server listening: {}",
        "app_worker_stopped": "Background analysis worker stopped",
        "app_shutting_down": "Shutting down...",
        "app_shutdown_complete": "Shutdown complete",
        "app_error_detail": "Error detail: {}",
        "app_fatal_error": "Fatal error: {}",
        "app_frontend_ready": "Frontend build ready",
        "app_frontend_not_ready": "Frontend static assets not ready, continuing FastAPI startup (web UI may be unavailable)",
        "app_frontend_build_failed": "Frontend command failed (exit_code={exit_code}): {cmd}",
        "app_frontend_building": "Building frontend assets...",
        "app_scheduler_thread": "Scheduler thread",
        "app_analysis_complete": "{} analysis complete",
        "app_analysis_failed": "{} analysis failed",

        "log_prefix_info": "INFO",
        "log_prefix_warn": "WARN",
        "log_prefix_error": "ERROR",
        "log_prefix_debug": "DEBUG",

        "api_internal_error": "Internal server error",
        "api_not_found": "Not found",
        "api_bad_request": "Invalid request parameters",
        "api_unauthorized": "Unauthorized",
        "api_forbidden": "Forbidden",
        "api_too_many_requests": "Too many requests",

        "notif_channel_wechat": "WeChat Work",
        "notif_channel_feishu": "Feishu",
        "notif_channel_telegram": "Telegram",
        "notif_channel_email": "Email",
        "notif_channel_slack": "Slack",
        "notif_send_success": "Notification sent ({channel})",
        "notif_send_failure": "Notification failed ({channel}): {detail}",
        "notif_channel_disabled": "Notification channel disabled: {channel}",

        "analysis_submitted": "Submitted {symbol} analysis task: {task_id}",
        "analysis_task_queued": "Analysis task queued: {task_id}",
        "analysis_task_running": "Analyzing: {symbol}",
        "analysis_task_complete": "Analysis complete: {symbol}",
        "analysis_task_failed": "Analysis failed: {symbol} - {detail}",
        "analysis_no_results": "No analysis results",
        "market_morning_greeting": "Good morning",
        "market_afternoon_greeting": "Good afternoon",
        "market_evening_greeting": "Good evening",
        "market_session_morning": "Morning session",
        "market_session_afternoon": "Afternoon session",
        "market_session_closed": "Market closed",
        "market_session_pre": "Pre-market",
        "market_session_post": "After-hours",
        "market_closed_today": "Market closed today",
        "market_open_today": "Market open today",

        "scheduler_starting": "Starting task scheduler...",
        "scheduler_started": "Task scheduler started",
        "scheduler_stopped": "Task scheduler stopped",
        "scheduler_next_run": "Next run: {time}",
        "scheduler_skip_holiday": "Market closed today, skipping scheduled tasks",
        "scheduler_task_start": "Starting scheduled task: {name}",
        "scheduler_task_done": "Scheduled task complete: {name}",
        "scheduler_task_failed": "Scheduled task failed: {name} - {detail}",

        "data_fetch_start": "Fetching {symbol} data from {source}...",
        "data_fetch_done": "{source} data fetch complete: {symbol} ({count} records)",
        "data_fetch_failed": "Data fetch failed ({source}): {detail}",
        "data_fetch_empty": "{source} returned no data for {symbol}",
        "data_fetch_rate_limited": "{source} rate limited, retrying in {seconds}s",
        "data_source_fallback": "{source} unavailable, falling back to {fallback}",
        "data_cache_hit": "Cache hit: {key}",
        "data_cache_miss": "Cache miss: {key}",

        "app_bootstrap_log_failed": "Bootstrap log init failed, falling back to stderr: {}",
        "app_config_load_failed": "Failed to load config: {}",
        "app_log_switch_failed": "Failed to switch to config log directory: {}",
        "app_system_start": "A-share Stock Analysis System starting",
        "app_runtime": "Runtime: {}",
        "app_market_review_running": "Market review already in progress, skipping",
        "app_stock_index_refreshed": "[stock-index] Stock index cache refreshed before analysis: {}",
        "app_stock_index_incomplete": "[stock-index] Index refresh incomplete, continuing with local index: {}",
        "app_stock_index_failed": "[stock-index] Stock index refresh failed, continuing analysis: {}",
        "app_all_markets_holiday": "All relevant markets are closed today. Use --force-run to override.",
        "app_holiday_skipped": "Holiday stocks skipped: {}",
        "app_context_reuse_skip": "Context reusable, skipping duplicate market review.",
        "app_context_reuse_push_ok": "Reused market context push succeeded",
        "app_context_reuse_push_fail": "Reused market context push failed",
        "app_waiting_market_review": "Waiting {}s before market review (API rate limit)...",
        "app_combined_push_ok": "Combined push sent (stocks + market review)",
        "app_combined_push_fail": "Combined push failed",
        "app_summary_header": "===== Analysis Summary =====",
        "app_execution_done": "Execution complete",
        "app_creating_feishu_doc": "Creating Feishu document...",
        "app_feishu_doc_created": "Feishu document created: {}",
        "app_feishu_doc_failed": "Feishu document generation failed: {}",
        "app_feishu_doc_notify": "[{}] Market review document: {}",
        "app_auto_backtest_start": "Starting auto backtest...",
        "app_auto_backtest_done": "Auto backtest complete: processed={processed} saved={saved} failed={failed}",
        "app_auto_backtest_failed": "Auto backtest failed (ignored): {}",
        "app_analysis_flow_failed": "Analysis flow failed: {}",
        "app_fastapi_exited": "FastAPI server exited immediately after start: {}",
        "app_fastapi_timeout": "FastAPI server did not start within {}s: {}",
        "app_schedule_stocks_param": "--stocks detected in schedule mode; startup snapshot will be ignored and STOCK_LIST re-read before each run.",
        "app_cli_stock_list": "Using CLI-specified stock list: {}",
        "app_config_loading": "Loading configuration...",
        "app_config_validating": "Validating configuration...",
        "app_market_review_reuse_fail": "Failed to save market review report from context reuse: {}",
        "app_score_format": "Score {score} | {trend}",
        "app_web_not_started": "Web UI not started (use --serve to enable)",
        "app_feishu_lock": "Feishu document generation disabled or lock failed, skipping",
        "app_config_file_fail": "Failed to read config file {}, continuing with environment variables: {}",
        "app_log_init_fail": "File log init failed, downgraded to console output; log dir {dir!r} is not writable or cannot be created: {exc}. Official Docker image entrypoint auto-fixes default mount permissions; if this persists, check for --user, read-only mounts, rootless Docker, or NFS restrictions.",
        "app_user_interrupt": "User interrupted, exiting",
        "app_program_failed": "Program failed: {}",
        "app_web_startup_failed": "Failed to start FastAPI: {}",
        "app_web_running": "Web server running: {}",
        "app_api_trigger": "Trigger analysis via /api/v1/analysis/analyze",
        "app_api_docs": "API docs: {}",
        "app_ctrl_c_exit": "Press Ctrl+C to exit...",
        "app_mode_web_only": "Mode: Web only",
        "app_mode_backtest": "Mode: Backtest",
        "app_mode_market_review_only": "Mode: Market review only",
        "app_mode_web_api_scheduler": "Mode: Web/API runtime scheduler",
        "app_mode_schedule": "Mode: Scheduled tasks",
        "app_market_review_holiday": "All markets for market review are closed today. Use --force-run to override.",
        "app_scheduler_takeover": "Web/API runtime scheduler managing tasks; saved settings apply to current process",
        "app_daily_exec_time": "Daily execution time: {}",
        "app_run_immediately": "Run immediately on start: {}",
        "app_event_monitor": "[EventMonitor] {} alerts triggered this round",
        "app_context_reuse_msg": "Context reusable, skipping duplicate market review with context reuse.",
        "app_waiting_review": "Waiting {}s before market review (API rate limit)...",
    },
}


def _resolve_language(language: Optional[str] = None) -> str:
    """Resolve language from explicit arg, env var, or default to zh."""
    if language:
        return normalize_report_language(language)
    env_lang = os.environ.get("REPORT_LANGUAGE")
    if env_lang:
        return normalize_report_language(env_lang)
    return "zh"


def gt(key: str, *args: Any, language: Optional[str] = None, **params: Any) -> str:
    """Get a translated UI string by key.

    Args:
        key: Translation key in _GENERAL_TEXT.
        *args: Positional format parameters for {} placeholders.
        language: 'zh' or 'en'. Defaults to REPORT_LANGUAGE env var or 'zh'.
        **params: Named format parameters for {name} placeholders.

    Returns the translated string with params interpolated.
    Falls back to zh if key is missing in the target language.
    """
    lang = _resolve_language(language)
    text = _GENERAL_TEXT.get(lang, {}).get(key)
    if text is None:
        text = _GENERAL_TEXT.get("zh", {}).get(key, key)
    if args:
        text = text.format(*args)
    if params:
        text = text.format(**params)
    return text

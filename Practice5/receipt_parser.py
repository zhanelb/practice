import re
import json

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

prices = re.findall(r"\b\d{1,3}(?:\s\d{3})*,\d{2}\b", text)
print("PRICES FOUND:", len(prices))
print("FIRST 10 PRICES:", prices[:10])

lines = text.splitlines()
product_names = []
for i in range(len(lines) - 1):
    if re.fullmatch(r"\d+\.", lines[i].strip()):
        product_names.append(lines[i + 1].strip())
print("\nPRODUCTS FOUND:", len(product_names))
for name in product_names:
    print("-", name)

def to_float_money(s: str) -> float:
    return float(s.replace(" ", "").replace(",", "."))

total_match = re.search(r"ИТОГО:\s*\n\s*([\d\s]+,\d{2})", text)
total_from_receipt = total_match.group(1) if total_match else None

item_cost_strings = re.findall(r"Стоимость\s*\n\s*([\d\s]+,\d{2})", text)
calculated_total = sum(to_float_money(x) for x in item_cost_strings)
print("\nTOTAL FROM RECEIPT:", total_from_receipt)
print("CALCULATED TOTAL (from 'Стоимость'):", f"{calculated_total:.2f}")

dt_match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})", text)
datetime_str = dt_match.group(1) if dt_match else None
print("DATETIME:", datetime_str)

payment = None
if re.search(r"Банковская\s+карта", text, re.IGNORECASE):
    payment = "Bank card"
elif re.search(r"Наличные", text, re.IGNORECASE):
    payment = "Cash"
print("PAYMENT:", payment)

data = {
    "datetime": datetime_str,
    "payment_method": payment,
    "total_from_receipt": total_from_receipt,
    "total_calculated_from_cost_lines": f"{calculated_total:.2f}",
    "product_names": product_names,
    "all_prices_found": prices
}
print("\nJSON OUTPUT:")
print(json.dumps(data, ensure_ascii=False, indent=2))
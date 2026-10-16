NAME = "battery_info"
DESCRIPTION = "Показывает информацию о батарее ноутбука, включая процент заряда и время работы."
PARAMS = {}
DANGEROUS = False

def run():
    import subprocess

    try:
        result = subprocess.run(["powercfg", "/batteryreport"], capture_output=True, text=True, check=True)
        report_path = result.stderr.split('\n')[-2].strip()
        with open(report_path, 'r', encoding='utf-8') as f:
            report_content = f.read()
            import re
            charge_percent = re.search(r'<td>(\d+)%</td>', report_content).group(1)
            remaining_time = re.search(r'<td>(\d+:\d+:\d+)</td>', report_content).group(1)
            battery_info = f"Заряд батареи: {charge_percent}%\nОставшееся время работы: {remaining_time}"
        import os
        os.remove(report_path)
        return battery_info
    except Exception as e:
        return f"Ошибка при получении информации о батарее: {str(e)}"
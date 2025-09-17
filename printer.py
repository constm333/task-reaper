import datetime
import win32print

ticket_id = 1
header_lines = 3  # Number of blank lines before the ticket (adjust as needed)
footer_lines = 15  # Number of blank lines after the ticket (adjust as needed)

def format_task(task, subtasks=None, notes=None, ticket_number=None):
    lines = [f"* {task['title']}"]

    if subtasks:
        lines.append("--------------------------------")
        lines.append("Subtasks:")
        for sub in subtasks:
            lines.append(f"- {sub}")

    if notes:
        lines.append("--------------------------------")
        lines.append("Notes:")
        lines.append(notes)

    date = datetime.datetime.now().strftime("%d/%m/%y")
    ticket_num_display = ticket_number if ticket_number is not None else "?"

    ticket = f"""
   |\\__/,|   (`\\  
 _.|o o  |_   ) )
-(((---(((--------      {date}
================================
           TICKET #{ticket_num_display}
--------------------------------
{chr(10).join(lines)}
================================
"""
    return ticket

def send_to_printer(text):
    printer_name = "58M Thermal Printer"
    raw_data = text.encode('cp437', errors='replace')

    # Add header blank lines
    header = '\n' * header_lines
    # Add footer blank lines
    footer = '\n' * footer_lines

    # Combine header, text, and footer
    full_text = header + text + footer
    raw_data = full_text.encode('cp437', errors='replace')

    try:
        h_printer = win32print.OpenPrinter(printer_name)
        try:
            doc_info = ("Task Ticket", None, "RAW")
            h_job = win32print.StartDocPrinter(h_printer, 1, doc_info)
            win32print.StartPagePrinter(h_printer)
            bytes_written = win32print.WritePrinter(h_printer, raw_data)
            win32print.EndPagePrinter(h_printer)
            win32print.EndDocPrinter(h_printer)
            print(f"✅ Ticket sent to printer! ({bytes_written} bytes written)")
        finally:
            win32print.ClosePrinter(h_printer)
    except Exception as e:
        print(f"⚠️ Failed to print, falling back to terminal output: {e}")
        print(text)

# Example usage
if __name__ == "__main__":
    sample_task = {'title': 'Test Task', 'notes': 'This is a note'}
    send_to_printer(format_task(sample_task))
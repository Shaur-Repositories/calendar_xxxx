import calendar
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch,cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime


def create_calendar(year):
    """
    Creates a calendar PDF for the given year.
    """

    # Create a PDF canvas with a letter page size
    c = canvas.Canvas(f"Calendar_{year}.pdf", pagesize=A4)
    # Set the title of the PDF document
    c.setTitle(f"Calendar {year}")

    try:
        # Register the Arial font for use in the PDF
        pdfmetrics.registerFont(TTFont('Poppins-Bold', 'Poppins-Bold.ttf'))
        pdfmetrics.registerFont(TTFont('Poppins', 'Poppins-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('Lato-Thin', 'Lato-Thin.ttf'))
        pdfmetrics.registerFont(TTFont('Lato', 'Lato-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

    except:
        print("Font(s) not found. Using default font.")

    def draw_mini_calendar(month, year, x, y):
        """
        Draws a mini calendar for a given month and year at the specified coordinates.
        """

        # Save the current state of the canvas
        c.saveState()
        # Translate the canvas origin to the given x, y coordinates
        c.translate(x, y)

        # Set the fill color for the mini calendar background
        c.setFillColor(colors.Color(248 / 255.0, 248 / 255.0, 248 / 255.0))
        # Draw a rectangle for the background
        c.setStrokeColor(colors.Color(248 / 255.0, 248 / 255.0, 248 / 255.0))
        c.rect(-0.2 * inch, 0, 1.1 * inch, 0.9 * inch, fill=1)

        # Set the fill color to black for the text
        c.setFillColor(colors.black)
        # Get the abbreviated month name in uppercase
        month_abbr = datetime(year, month, 1).strftime("%b").upper()
        # Set the font to Arial with size 8
        c.setFont("Lato", 8)
        # Draw the month and year string
        c.drawCentredString(0.4 * inch, 0.8 * inch, f"{month_abbr} {year}")

        # List of days of the week abbreviations
        days_abbr = ["S", "M", "T", "W", "T", "F", "S"]
        x_offset = -0.13 * inch
        # Loop through the days of the week and draw each abbreviation
        for day in days_abbr:
            c.setFont("Lato", 6)
            c.drawCentredString(x_offset, 0.65 * inch, day)
            x_offset += 0.17 * inch

        # Get the calendar for the month
        calendar.setfirstweekday(6) #change first day of week as sunday
        cal = calendar.monthcalendar(year, month)

        y_offset = 0.45 * inch
        # Loop through the weeks in the calendar
        for week in cal:
            x_offset = -0.12 * inch
            # Loop through the days in the week
            for day in week:
                # If the day is not 0 (i.e., it's a valid day)
                if day != 0:
                    c.setFont("Poppins", 6)
                    c.drawCentredString(x_offset, y_offset, str(day))
                x_offset += 0.17 * inch
            y_offset -= 0.12 * inch

        # Restore the saved state of the canvas
        c.restoreState()

    def draw_month_calendar(month, year):
        """
        Draws the main calendar for the given month and year.
        """

        # Save the current state of the canvas
        c.saveState()

        # --- Header ---
        header_y = 10 * inch  # Further reduce space from top
        c.setFont("Poppins-Bold", 80)
        c.drawString(0.5*inch +3, header_y, f"{month:02}.")

        c.setFont("Lato-Thin", 20)
        month_name = datetime(year, month, 1).strftime("%B").upper()
        c.drawString(0.5*inch+3, header_y - 0.3 * inch, f"{month_name} {year}")  # Reduced space after month

        # --- Days of the Week ---
        days = ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]
        x_position = inch + 5
        days_y = 9.45 * inch # Bring days of week closer to header
        for day in days:
            c.setFont("Lato", 10)
            c.drawCentredString(x_position, days_y, day)
            x_position += 1.03 * inch  # Adjust for tighter spacing

        # --- Calendar Grid ---
        calendar.setfirstweekday(6) #change first day of week as sunday
        cal = calendar.monthcalendar(year, month)
        x_start = inch + 3
        y_start = 9.4 * inch # Bring calendar grid closer to days
        cell_width = 1.03 * inch
        cell_height = 1.25 * inch
        spacing = 0.06 * inch  # Increase space between cells
        #day_num_y_offset = 0.2 * inch # Offset to position day numbers inside the cell

        # Loop through the weeks in the calendar
        weeks_in_month = len(cal)
        grid_height = weeks_in_month * cell_height # Total height of the grid

        for week in cal:
            x_position = x_start
            for day in week:
                # Set the fill color for the calendar cell
                c.setFillColor(colors.Color(248 / 255.0, 248 / 255.0, 248 / 255.0))
                # Draw a rectangle for the calendar cell
                c.setStrokeColor(colors.Color(248 / 255.0, 248 / 255.0, 248 / 255.0))
                c.rect(x_position - (cell_width / 2) + spacing/2, y_start - cell_height + spacing/2,
                       cell_width - spacing, cell_height - spacing, fill=1)

                # If the day is not 0 (i.e., it's a valid day)
                if day != 0:
                    # Set the font and fill color for the day number
                    c.setFont("Poppins", 10)
                    c.setFillColor(colors.black)
                    # Draw the day number
                    c.drawRightString(x_position + (cell_width / 2) - (0.1 * inch),
                                      y_start - (cell_height / 4) + (0.1 * inch), str(day))
                x_position += cell_width

            y_start -= cell_height

        # --- Notes Section ---
        notes_x = 0.5 * inch  + 3
        # Position the notes section right below the calendar grid
        notes_y = y_start - 0.345 * inch # 0.1 inch spacing from the last cell
        print("########");
        w, h = A4
        len_to_use = (h - 0.5*inch) - (h - y_start) - 8
        print(len_to_use)
        notes_width = cell_width * 4.5

        # Set the fill color for the notes section background
        c.setFillColor(colors.Color(248 / 255.0, 248 / 255.0, 248 / 255.0))
        # Draw a rectangle for the notes section background
        c.setStrokeColor(colors.Color(248 / 255.0, 248 / 255.0, 248 / 255.0))
        c.rect(notes_x, notes_y - len_to_use + 23 , notes_width,
               len_to_use, fill=1)

        #y top = notes_y - (cell_height)- inch /5
        # y = cell_height / 2 + (cell_height / 4) + inch / 5

        # Set the font and fill color for the notes text
        c.setFont("Lato", 10)
        c.setFillColor(colors.black)
        # Draw the "NOTES" text at the top-left
        c.drawString(notes_x + (cell_width / 10) - 0.05 * inch, notes_y - (cell_height / 8) + 0.3 * inch, "NOTES")

        # --- Mini Calendars Section ---
        mini_calendar_x = notes_x + notes_width + (cell_width / 4)
        # Position the mini calendars at the same level as the notes
        mini_calendar_y = notes_y

        len_to_use_1 = len_to_use
        
        if len_to_use > 100 :
            len_to_use_1 = len_to_use/2

        # Define dimensions for combined background of the mini calendars
        combined_bg_width = 2.5 * inch  # Adjust as needed
        combined_bg_height = len_to_use_1
        # Set the fill color for the mini calendars section background
        c.setFillColor(colors.Color(248 / 255.0, 248 / 255.0, 248 / 255.0))
        # Draw a rectangle for the combined background of the mini calendars
        c.setStrokeColor(colors.Color(248 / 255.0, 248 / 255.0, 248 / 255.0))
        c.rect(mini_calendar_x - 0.2 * inch, notes_y - (len_to_use_1 )+ 23, combined_bg_width, combined_bg_height , fill=1)
        if len_to_use > 100 :
            c.rect(mini_calendar_x - 0.2 * inch, notes_y + (1.12 * inch)- (len_to_use ) +30 , combined_bg_width, (  0.06* inch) - combined_bg_height  , fill=1)

        # Calculate the months and years for the mini calendars
        next_month1 = (month % 12) + 1
        next_year1 = year + (month // 12)
        next_month2 = (next_month1 % 12) + 1
        next_year2 = year + ((month + 1) // 12)

        # Draw the mini calendars for the next two months
        draw_mini_calendar(next_month1, next_year1, mini_calendar_x, notes_y - (cell_height/2))
        draw_mini_calendar(next_month2, next_year2, mini_calendar_x + 1.3 * inch, notes_y - (cell_height/2))

        # Bottom Line
        line_y = notes_y - 1.3 * inch  # Position relative to notes
        c.setStrokeColor(colors.black)
        #c.line(0.5*inch, line_y, 7.65 * inch, line_y)
        c.setFillColorRGB(0,0,0)
        c.rect(0.5*inch + 3 , inch * 0.5, 18.1*cm, 2, stroke=1, fill=1)
        c.circle(19.6*cm ,inch * 0.5 +1.25 , 1.25, stroke=1, fill=1)

        # Restore the saved state of the canvas
        c.restoreState()
        # Show the page
        c.showPage()

    # Generate the calendar for each month in the year
    for month in range(1, 13):
        draw_month_calendar(month, 2025)

    # Save the PDF to a file
    c.save()

# Get the year from the user
#year = int(input("Enter the year for which you want to generate the calendar: "))
# Create the calendar
create_calendar(2025)

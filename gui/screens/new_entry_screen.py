import datetime
from tkinter import Entry, Frame, Label, StringVar, Text
from tkinter import ttk

from domain.fields import FIELDS
from gui.screens.screen import Screen

ENTRY_FIELDS = [field for field in FIELDS if field != "date"]
MULTILINE_FIELDS = {"work_contribution", "learning"}


class NewEntryScreen(Screen):
    TEXT_HEIGHT = 4

    def __init__(self, *args, on_home, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_home = on_home
        self._text_widgets = {}

        self._configure_grid()
        self._create_header_row()
        self._create_date_dropdown()
        self._create_fields_frame()
        self._create_save_button()

    def _configure_grid(self):
        """Single column; header, date, fields, and save button stack vertically."""
        self._configure_responsive_grid(
            col_dict={0: 1, 1: 1},
            row_dict={0: 0, 1: 0, 2: 1, 3: 0}
        )

    def _create_header_row(self):
        """Title label on the left, back button on the right."""
        self.title_label = Label(
            self, text="NEW ENTRY",
            font=self.heading_font,
            fg=self.SECONDARY_COLOR,
            bg=self.PRIMARY_COLOR,
            anchor="w",
        )
        self.title_label.grid(
            row=0, column=0, padx=(self.OUTER_PADDING, 10),
            pady=(20, 10), sticky="w"
        )

        back_btn = self._add_back_button(func=self._on_home)
        self._position_button(
            back_btn, row=0, column=1, colspan=1,
            pad_x=(10, self.OUTER_PADDING), pad_y=(20, 10), sticky="e"
        )

    def _create_date_dropdown(self):
        """Centred date dropdown spanning both columns."""
        date_frame = Frame(self, bg=self.PRIMARY_COLOR)
        date_frame.grid(
            row=1, column=0, columnspan=2,
            padx=self.OUTER_PADDING, pady=(0, 10), sticky="ew"
        )
        date_frame.grid_columnconfigure(0, weight=1)

        Label(
            date_frame, text="Date",
            font=self.subheading_font,
            fg=self.SECONDARY_COLOR,
            bg=self.PRIMARY_COLOR,
        ).grid(row=0, column=0, pady=(0, 4))

        today = datetime.date.today()
        dates = [
            (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(365)
        ]
        self._date_var = StringVar(value=dates[0])
        date_dropdown = ttk.Combobox(
            date_frame, textvariable=self._date_var,
            values=dates, state="readonly", width=20
        )
        date_dropdown.grid(row=1, column=0)

    def _create_fields_frame(self):
        """Light-blue bordered outer frame containing a white inner frame with labelled entry fields."""
        self.fields_frame = self._create_frame(row=2, column=0, colspan=2)

        inner = self._create_inner_frame(self.fields_frame)
        inner.grid_columnconfigure(0, weight=1)
        inner.grid_columnconfigure(1, weight=3)

        for i, field in enumerate(ENTRY_FIELDS):
            inner.grid_rowconfigure(i, weight=1)
            is_multiline = field in MULTILINE_FIELDS

            # Labels next to a tall Text widget are pinned to the top-left with
            # matching top padding so they align with the first line of text.
            # Labels next to a single-line Entry are truly vertically centred with sticky="w".
            label_sticky = "nw" if is_multiline else "w"
            label_pady = (14, 10) if is_multiline else 10

            Label(
                inner,
                text=field.upper().replace("_", " ") + ":",
                font=self.subheading_font,
                bg="white",
                anchor="w",
            ).grid(row=i, column=0, padx=(20, 10), pady=label_pady, sticky=label_sticky)

            if is_multiline:
                widget = Text(
                    inner,
                    height=self.TEXT_HEIGHT,
                    font=self.italic_font,
                    relief="solid",
                    borderwidth=1,
                    wrap="word",
                )
                widget.grid(row=i, column=1, padx=(0, 20), pady=10, sticky="ew")
            else:
                widget = Entry(
                    inner,
                    font=self.italic_font,
                    relief="solid",
                    borderwidth=1,
                )
                widget.grid(row=i, column=1, padx=(0, 20), pady=10, sticky="ew")

            self._text_widgets[field] = widget

    def _create_save_button(self):
        """Save button centred at the bottom with a fixed width."""
        container = Frame(self, bg=self.PRIMARY_COLOR)
        container.grid(row=3, column=0, columnspan=2, pady=(10, 60))

        save_btn = self._create_stylised_button(
            parent=container,
            title="✔️ Save",
            subtitle="Save entry & return to Home",
            func=self._on_save
        )
        save_btn.grid(padx=self.OUTER_PADDING)

    def _on_save(self):
        """Collect field values and submit via the save callback."""
        pass

    def get_entry_data(self):
        """Return a dict of the current date and field values."""
        data = {"date": self._date_var.get()}
        for field, widget in self._text_widgets.items():
            if isinstance(widget, Text):
                data[field] = widget.get("1.0", "end-1c").strip()
            else:
                data[field] = widget.get().strip()
        return data

    def clear_fields(self):
        """Clear all fields and reset date to today."""
        today = datetime.date.today().strftime("%Y-%m-%d")
        self._date_var.set(today)
        for widget in self._text_widgets.values():
            if isinstance(widget, Text):
                widget.delete("1.0", "end")
            else:
                widget.delete(0, "end")

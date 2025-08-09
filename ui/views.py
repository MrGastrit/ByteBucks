from discord.ui import Button, Modal, View, Select
import discord



class DropdownView(View):
    def __init__(self, placeholder: str, options: list[discord.SelectOption], callback):
        super().__init__(timeout=None)

        self.options = options

        self.select = Select(placeholder=placeholder, options=options)

        self.select.callback = self.select_callback
        self.callback = callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        selected = self.select.values[0]
        await self.callback(interaction, self.options, selected)



class ButtonView(View):
    def __init__(self, label: str, options, product,  callback, button_style):
        super().__init__(timeout=60)
        self.options = options
        self.product = product
        self.callback = callback

        button = Button(label=label, style=button_style)
        button.callback = self.button_callback
        self.add_item(button)

    async def button_callback(self, interaction: discord.Interaction):
        await self.callback(interaction, self.options, self.product)
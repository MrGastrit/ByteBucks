from discord.ext import commands
from discord import app_commands, SelectOption
from utils.database import *
from datetime import datetime, timedelta, timezone
from ui.views import *

import psycopg2
import discord
import os
from dotenv import load_dotenv

load_dotenv("important.env")


conn = psycopg2.connect(user=os.getenv("USER"), password=os.getenv("DB_PASS"), host="localhost", port="5432", database=os.getenv("DATABASE"))
cursor = conn.cursor()


class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shop", description="Открыть магазин")
    @app_commands.checks.has_permissions(send_messages=True)
    async def shop(self, interaction: discord.Interaction):
        async def handle_purchase_accept(interaction: discord.Interaction, options, product):
            label = next((opt.label for opt in options if opt.value == product), product)

            splited = label.split(" - ")
            price = splited[1].replace(" ", "")

            if get_balance(interaction.user.id) >= int(price):
                set_balance(interaction.user.id, get_balance(interaction.user.id) - int(price))
                await interaction.response.edit_message(content="🛒 Оплата прошла! Удачного пользования!", view=None)

                add_item(interaction.user.id, product)
            else:
                await interaction.response.edit_message(content="💳 На вашем балансе недостаточно средств! Иди работай, потом приходи.", view=None)

        async def handle_product_selection(interaction: discord.Interaction, options, product: str):
            label = next((opt.label for opt in options if opt.value == product), product)

            splited = label.split(" - ")

            await interaction.response.send_message(f"🛒 Вы выбрали товар: {splited[0]}\nНажмите на кнопку, чтобы подтвердить оплату", view=ButtonView("Подтвердить", options, product, handle_purchase_accept, discord.ButtonStyle.success), ephemeral=True)

        async def handle_selection(interaction: discord.Interaction, options, selected: str):
            if selected == "electronics":
                embed = discord.Embed(description="## Категория - __💻 Электроника__", color=discord.Color.dark_teal())
                options = [
                    SelectOption(label="🎥 Камера - 15999", value="camera"),
                    SelectOption(label="💻 Ноутбук ASAS - 49500", value="laptop"),
                    SelectOption(label="💻 Macback Air M4 Pro - 119000", value="laptop"),
                    SelectOption(label="📱 Смартфон - 11999", value="phone"),
                    SelectOption(label="🪫 Повербанк - 2199", value="powerbank"),
                ]
                await interaction.response.edit_message(embed=embed, view=DropdownView("Выбрать товар", options, handle_product_selection))

            elif selected == "sports":
                embed = discord.Embed(description="## Категория - __🚴 Спорттовары__", color=discord.Color.dark_teal())
                options = [
                    SelectOption(label="👟 Беговые кроссовки - 3990", value="boots"),
                    SelectOption(label="🚲 Велосипед - 13999", value="bicycle"),
                    SelectOption(label="🥤 Бутылка воды - 255", value="waterbottle"),
                    SelectOption(label="📜 Абонемент в спортзал - 4799", value="gymmembership"),
                    SelectOption(label="⚽ Мяч - 1870", value="ball"),
                ]
                await interaction.response.edit_message(embed=embed, view=DropdownView("Выбрать товар", options, handle_product_selection))

            elif selected == "office":
                embed = discord.Embed(description="## Категория - __🖋️ Канцелярия__", color=discord.Color.dark_teal())
                options = [
                    SelectOption(label="🖋️ Ручка - 199", value="pen"),
                    SelectOption(label="🖌️ Кисть - 990", value="brush"),
                    SelectOption(label="✏️ Карандаш - 89", value="pencil"),
                    SelectOption(label="🖊️ Продвинутая ручка - 9990", value="bestpen"),
                    SelectOption(label="✂️ Ножницы - 279", value="scissors"),
                    SelectOption(label="📃 Холст - 3260", value="canvas"),
                    SelectOption(label="🎨 Краски - 4890", value="paints"),
                    SelectOption(label="📖 Пустая книга - 875", value="emptybook"),

                ]
                await interaction.response.edit_message(embed=embed, view=DropdownView("Выбрать товар", options, handle_product_selection))

            elif selected == "tools":
                embed = discord.Embed(description="## Категория - __🔨 Инструменты__", color=discord.Color.dark_teal())
                options = [
                    SelectOption(label="🧰 Набор инструментов - 4850", value="toolset"),
                    SelectOption(label="🥼 Рабочая форма - 5149", value="uniform"),
                ]
                await interaction.response.edit_message(embed=embed, view=DropdownView("Выбрать товар", options, handle_product_selection))

            elif selected == "fun":
                embed = discord.Embed(description="## Категория - __🎮 Развлечения__", color=discord.Color.dark_teal())
                options = [
                    SelectOption(label="🎮 Игровая консоль - 52500", value="console"),
                    SelectOption(label="🃏 Игральные карты - 229", value="cards"),
                ]
                await interaction.response.edit_message(embed=embed, view=DropdownView("Выбрать товар", options, handle_product_selection))

            elif selected == "other":
                embed = discord.Embed(description="## Категория - __🗿 Другое__", color=discord.Color.dark_teal())
                options = [
                    SelectOption(label='⌚ Часы "RoleRx" - 1 675 000', value="rolerx"),
                    SelectOption(label='🚗 Автомобиль "Royce Royce" - 7 490 000', value="royce"),
                    SelectOption(label="🏡 Дом в горах - 24 700 000", value="house"),
                ]
                await interaction.response.edit_message(embed=embed, view=DropdownView("Выбрать товар", options, handle_product_selection))

        embed = discord.Embed(title="Магазин", description="Здесь вы можете купить всё, что вам нужно (почти всё)", color=discord.Color.dark_teal())
        options = [
            SelectOption(label="💻 Электроника", value="electronics"),
            SelectOption(label="🚴 Спорттовары", value="sports"),
            SelectOption(label="🖋️ Канцелярия", value="office"),
            SelectOption(label="🔨 Инструменты", value="tools"),
            SelectOption(label="🎮 Развлечения", value="fun"),
            SelectOption(label="🗿 Другое", value="other"),
        ]
        await interaction.response.send_message(embed=embed, view=DropdownView("Выбрать категорию товаров", options, handle_selection))


    @app_commands.command(name="works", description="Центр занятости")
    @app_commands.checks.has_permissions(send_messages=True)
    async def works(self, interaction: discord.Interaction):
        async def handle_prof_accept(interaction: discord.Interaction, options, prof):
            label = next((opt.label for opt in options if opt.value == prof), prof)

            match prof:
                case "artist" | "writer" | "mechanic" | "programmer" | "blogger":
                    await try_set_job(interaction, prof, label)


        async def handle_prof_selection(interaction: discord.Interaction, options, product: str):
            label = next((opt.label for opt in options if opt.value == product), product)

            await interaction.response.send_message(f"Вы выбрали профессию: {label}\nНажмите на кнопку, чтобы устроиться на работу", view=ButtonView("Подтвердить", options, product, handle_prof_accept, discord.ButtonStyle.success), ephemeral=True)

        async def handle_selection(interaction: discord.Interaction, options, selected: str):
            embed = discord.Embed(title="", description="## Центр занятости населения \n ### 🤝 Выберите подходящую для вас вакансию", color=discord.Color.dark_gold())

            if selected == "fornews":
                options = [
                    SelectOption(label="🚶 Курьер", value="courier"),
                    SelectOption(label="🧹 Уборщик", value="cleaner"),
                    SelectOption(label="🍔 Работник фастфуда", value="fastfood"),
                    SelectOption(label="📦 Грузчик", value="loader"),
                ]
                await interaction.response.edit_message(embed=embed, view=DropdownView("Выбрать работу", options, handle_prof_selection))

            elif selected == "preparation":
                options = [
                    SelectOption(label="🎨 Художник", value="artist"),
                    SelectOption(label="✍️ Писатель", value="writer"),
                    SelectOption(label="🔧 Механик", value="mechanic"),
                    SelectOption(label="💻 Программист", value="programmer"),
                    SelectOption(label="📹 Видеоблогер", value="blogger"),
                ]
                await interaction.response.edit_message(embed=embed, view=DropdownView("Выбрать работу", options, handle_prof_selection))



        embed = discord.Embed(title="", description="## Центр занятости населения \n ### 🤝 Здесь вы можете устроиться на работу", color=discord.Color.dark_gold())
        options = [
            SelectOption(label="🚶 Для новичков", value="fornews"),
            SelectOption(label="📋 Требующие подготовки", value="preparation")
        ]

        await interaction.response.send_message(embed=embed, view=DropdownView("Выбрать категорию", options, handle_selection))


        JOB_REQUIREMENTS = {
            "artist": ["paints", "canvas", "brush"],
            "writer": ["emptybook", "pen"],
            "mechanic": ["toolset", "uniform"],
            "programmer": ["laptop"],
            "blogger": ["camera"],
        }

        async def try_set_job(interaction: discord.Interaction, prof, label):
            if not get_need_items(interaction.user.id, JOB_REQUIREMENTS[prof]):
                await interaction.response.edit_message(content="У вас нет нужных предметов", view=None)
                return
            if get_job(interaction.user.id) is not None:
                await interaction.response.edit_message(content="У вас уже есть работа!", view=None)
                return

            set_job(interaction.user.id, prof)
            await interaction.response.edit_message(content=f"Поздравляем! Вы устроились на работу: {label}", view=None)


async def setup(bot):
    await bot.add_cog(EconomyCog(bot))

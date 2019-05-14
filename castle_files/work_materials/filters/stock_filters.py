"""
Здесь назодятся фильтры для работы со стоком
"""
from telegram.ext import BaseFilter
from castle_files.work_materials.filters.general_filters import filter_is_pm, filter_is_chat_wars_forward


# Сообщение - форвард /g_stock_rec из чв3 и в личке
class FilterGuildStockRecipes(BaseFilter):
    def filter(self, message):
        return message.forward_from and filter_is_chat_wars_forward(message) and\
               filter_is_pm(message) and message.text.find("Guild Warehouse:") == 0 and "recipe" in message.text


filter_guild_stock_recipes = FilterGuildStockRecipes()


# Сообщение - форвард /g_stock_parts из чв3 и в личке
class FilterGuildStockParts(BaseFilter):
    def filter(self, message):
        return message.forward_from and filter_is_chat_wars_forward(message) and \
               filter_is_pm(message) and message.text.find("Guild Warehouse:") == 0 and "part" in message.text


filter_guild_stock_parts = FilterGuildStockParts()
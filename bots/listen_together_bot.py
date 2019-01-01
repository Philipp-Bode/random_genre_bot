from spotipy import SpotifyException
from telegram.ext import (
    Filters,
    Updater,
    MessageHandler,
)

from spotify_telegram_bot import (
    SpotifyTelegramBot,
    spotify_action,
)


class ListenTogetherBot(SpotifyTelegramBot):

    @staticmethod
    @spotify_action
    def select(client, bot, update, chat_data):

        text = update.message.text

        if text.startswith('https://open.spotify.com/'):
            try:
                track = client.track(text)
                uri = track['uri']
            except SpotifyException:
                uri = None
        elif text.startswith('spotify:'):
            uri = text
        else:
            uri = None

        client.start_playback(
            uris=[uri])
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f'Now listening to: {uri}'
        )

    @classmethod
    def handlers(cls):
        return super().handlers() + (
            MessageHandler(Filters.text, cls.select, pass_chat_data=True),
        )


if __name__ == '__main__':

    updater = Updater(token=ListenTogetherBot.TOKEN)
    dispatcher = updater.dispatcher
    for handler in ListenTogetherBot.handlers():
        dispatcher.add_handler(handler)
    updater.start_polling()

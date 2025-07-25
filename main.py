import asyncio
from app.infra.logs.sentry import init_sentry
from app.infra.telegram.bot import create_bot, set_metadata
from app.infra.telegram.scheduler_hub import create_scheduler
from app.infra.telegram.dispatcher_hub import create_dispatcher


async def main():

    bot = create_bot()

    async with bot:
        await set_metadata(bot)
        dp = create_dispatcher()

        scheduler = create_scheduler(bot)
        scheduler.start()

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ == "__main__":
    init_sentry()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("App terminated manually")
    except Exception as e:
        print(f"Launching error | {type(e).__name__} | {e}")

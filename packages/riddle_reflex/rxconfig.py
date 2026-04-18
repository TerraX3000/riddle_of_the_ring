import reflex as rx

config = rx.Config(
    app_name="riddle_reflex",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)
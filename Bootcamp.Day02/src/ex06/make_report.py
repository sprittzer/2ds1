import sys, logging
from analytics import Research, Analytics
import config

def setup_logging():
    logging.basicConfig(
        filename='analytics.log',
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def main():
    setup_logging()
    
    if len(sys.argv) != 2:
        print("Usage: python3 first_constructor.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    research_obj = Research(file_path)
    success = False

    try:
        data = research_obj.file_reader(has_header=config.has_header)
        analytics_obj = Analytics(data)
        
        calculator = research_obj.Calculations(data)
        
        heads, tails = calculator.counts()
        
        heads_pct, tails_pct = calculator.fractions(heads, tails)
        
        predictions = analytics_obj.predict_random(config.predictions_number)
        heads_forecast = sum(1 for p in predictions if p == [1, 0])
        tails_forecast = sum(1 for p in predictions if p == [0, 1])
        
        resulting_text = config.resulting_file__text.format(
            total_observations=len(data),
            tails_count=tails,
            heads_count=heads,
            tails_percent=tails_pct,
            heads_percent=heads_pct,
            tails_forecast=tails_forecast,
            heads_forecast=heads_forecast
        )
        analytics_obj.save_file(resulting_text, config.resulting_file_name, config.resulting_file_expansion)
        success = True
    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error in main: {e}")
    finally:
        research_obj.send_telegram_message(success, config.tg_webhook_url, config.tg_chat_id)
        
if __name__ == "__main__":
    main()
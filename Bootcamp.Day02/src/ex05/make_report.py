import sys
from analytics import Research, Analytics
import config

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 first_constructor.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    research_obj = Research(file_path)

    try:
        data = research_obj.file_reader(has_header=config.has_header)
        analytics_obj = Analytics(data)
        
        calculator = research_obj.Calculations(data)
        
        heads, tails = calculator.counts()
        
        heads_pct, tails_pct = calculator.fractions(heads, tails)
        
        predictions = analytics_obj.predict_random(config.predictions_number)
        heads_forecast, tails_forecast = research_obj.Calculations(predictions).counts()
        
        resulting_text = config.resulting_file__text.format(
            total_observations=len(data),
            tails_count=tails,
            heads_count=heads,
            tails_percent=tails_pct,
            heads_percent=heads_pct,
            steps=config.predictions_number,
            tails_forecast=tails_forecast,
            heads_forecast=heads_forecast
        )
        analytics_obj.save_file(resulting_text, config.resulting_file_name, config.resulting_file_expansion)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
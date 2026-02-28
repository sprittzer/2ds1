has_header = True
predictions_number = 5

resulting_file__text = (
    "We made {total_observations} observations by tossing a coin: {tails_count} were tails and {heads_count} were heads. "
    "The probabilities are {tails_percent:.2f}% and {heads_percent:.2f}%, respectively. Our forecast is that the "
    "next {steps} observations will be: {tails_forecast} tail(s) and {heads_forecast} head(s)."
    )
resulting_file_name = 'report'
resulting_file_expansion = 'txt'
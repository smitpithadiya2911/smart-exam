def format_rank(rank_int):
    if rank_int == 1:
        return "1st 🥇"
    elif rank_int == 2:
        return "2nd 🥈"
    elif rank_int == 3:
        return "3rd 🥉"
    return f"{rank_int}th"

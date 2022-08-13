import argparse
from datetime import datetime, timezone

# Get current UTC time
current_time = datetime.now(timezone.utc)
print(current_time)

parser = argparse.ArgumentParser(description="Download glm data from Google Cloud")

# positional arguments
parser.add_argument(
    "start_date", 
    help = "start of the time range we want to download", 
    type = lambda s: datetime.datetime.strptime("%Y-%m-%d")
)

parser.add_argument(
    "end_date", 
    help = "end of the time range we want to download", 
    type = lambda s: datetime.datetime.strptime("%Y-%m-%d")
)

parser.add_argument("--verbose", help="increase output verbosity", action="store_true")

args = parser.parse_args()


if args.verbose:
    print(args.square, "^ 2 =", end = " ")
print(args.square**2)


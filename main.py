from draw import animate_traj
from generate_reference import generate_reference
from traj_opt import traj_opt
import argparse
from distutils.util import strtobool
import time
from datetime import datetime

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--display",
        help="toggle whether to display animation window",
        type=strtobool,
        default=1,
    )
    parser.add_argument("-n", "--name", help="experiment name", type=str, default=None)
    parser.add_argument(
        "-s", "--save", help="toggle whether to save motion", type=strtobool, default=0
    )

    # parse and post processing
    args = parser.parse_args()
    args.display = bool(args.display)
    args.save = bool(args.save)
    if args.name is None:
        args.name = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

    # generate reference, optionally display/save animation
    X_ref, U_ref, dt = generate_reference()
    if args.save:
        fname_ref = args.name + "-ref"
    else:
        fname_ref = None
    animate_traj(X_ref, U_ref, dt, fname_ref, display=args.display)

    # solve trajectory optimization
    start_time = time.time()
    X_sol, U_sol = traj_opt(X_ref, U_ref, dt)
    print("\nOptimization took {} minutes".format((time.time() - start_time) / 60.0))

    # optionally display/save solution animation
    if args.save:
        fname = args.name
    else:
        fname = None
    animate_traj(X_sol, U_sol, dt, fname, display=args.display)
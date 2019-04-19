import os

import chalk
import click


@click.group()
def gif():
    """
        Create gif from images or video. Hi, my name is jif!!!

        This command takes arbitary number of arguments.
        All arguments except source and output are passed to imageio's save call.
        This can be used to alter gif export process.
        e.g.
        yoda gif from-images --source gif_frames/ --output test.gif --fps 30
        sets fps of the gif to 30/s.
    """


@gif.command(
    name="from-images",
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
)
@click.pass_context
def from_images(ctx):
    #importing imageio in theis function improves load time for all yoda commands
    import imageio

    args = {
        ctx.args[i].strip("--"): ctx.args[i + 1] for i in range(0, len(ctx.args), 2)
    }
    try:
        source = args.pop("source")
    except KeyError:
        click.echo(
            chalk.red(
                "Source parameter is missing. " "Use --source to provide the path."
            )
        )
        return
    try:
        output = args.pop("output")
    except KeyError:
        click.echo(
            chalk.red("Output path is missing. " "Use --output to provide the path.")
        )
        return
    images = []
    if not os.path.isdir(source):
        click.echo(chalk.red("Source should be a directory."))
    for filename in os.listdir(source):
        if os.path.isfile(os.path.join(source, filename)):
            images.append(imageio.imread(os.path.join(source, filename)))

    try:
        with open(output, "w") as outfile:
            imageio.mimsave(outfile, images, format="gif", **args)
        click.echo(chalk.green("GIF exported at {}".format(output)))
    except (OSError, IOError):
        click.echo(
            chalk.red(
                "Could not write to file {}. " "Please check the path".format(output)
            )
        )

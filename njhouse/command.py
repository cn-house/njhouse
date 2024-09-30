# coding:utf-8

from typing import Optional
from typing import Sequence

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from .attribute import __project__
from .attribute import __urlhome__
from .attribute import __version__
from .utils import njhouse_project
from .utils import njhouse_rent
from .utils import njhouse_stock


@add_command("query", help="查询数据")
def add_cmd_query(_arg: argp):
    pass


@run_command(add_cmd_query)
def run_cmd_query(cmds: commands) -> int:
    njh_project = njhouse_project()
    cmds.stdout(f"商品房认购：{njh_project.subscriptions}")
    cmds.stdout(f"商品房成交：{njh_project.transactions}")
    njh_stock = njhouse_stock()
    cmds.stdout(f"存量房总挂牌房源：{njh_stock.total_listings}")
    cmds.stdout(f"存量房中介挂牌房源：{njh_stock.intermediary_listings}")
    cmds.stdout(f"存量房个人挂牌房源：{njh_stock.personal_listings}")
    cmds.stdout(f"存量房昨日住宅成交量：{njh_stock.yesterday_tradings}")
    njh_rent = njhouse_rent()
    cmds.stdout(f"租赁房挂牌量：{njh_rent.listings}")
    return 0


@add_command(__project__)
def add_cmd(_arg: argp):
    pass


@run_command(add_cmd, add_cmd_query)
def run_cmd(cmds: commands) -> int:
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(
        root=add_cmd,
        argv=argv,
        description="抓取 njhouse.com.cn 数据",
        epilog=f"For more, please visit {__urlhome__}.")

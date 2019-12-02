import pymysql.cursors
from discord.ext import commands

from settings import *

bot = commands.Bot(command_prefix=".")


def connect_database():
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASS,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print('[*] Connected to database: %s' % DB_NAME)
    return connection


db = connect_database()


def get_player(user_id):
    try:
        with db.cursor() as cursor:
            sql = "SELECT `*` FROM `players` WHERE `user_id`=%s"
            cursor.execute(sql, user_id)
            result = cursor.fetchone()
            if not result:
                print("User does not exist: %s" % user_id)
            else:
                return result
    except Exception as e:
        print("Error looking up userid %s.\n%s" % (user_id, e))


def add_all_users_to_db():
    for member in bot.get_all_members():
        add_user_to_db(member)


def add_user_to_db(member):
    if get_player(member.id):
        return

    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO `players` (`user_id`, `join_server_date`, `bank`)" + \
                  " VALUES (%s, %s, %s)"
            cursor.execute(sql, (member.id, member.joined_at, 0))
        db.commit()
        print("Added user %s to database." % member.id)
    except Exception as e:
        print("Error adding user: %s" % e)


def update_bank(member, points):
    player_info = get_player(member.id)
    with db.cursor() as cursor:
        try:
            sql = "UPDATE players SET bank=%s WHERE user_id=%s"
            new_point_value = player_info['bank'] + points
            cursor.execute(sql, (new_point_value, member.id))
            db.commit()
            print("[*] Updated user %s bank account from %s to %s." %
                  (member.name, player_info['bank'], new_point_value))
        except Exception as e:
            print("[-] Error updating bank account for %s; %s" % (member.id, e))


def add_all_items_to_shop(data):
    for item in data:
        add_item_to_shop(item)


def add_item_to_shop(data):
    if get_item(data):
        return
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO `shop` (`item`, `price`)" + \
                  " VALUES (%s, %s)"
            for key, value in data.items():
                cursor.execute(sql, (key, value))
                db.commit()
                print("Added item %s to database." % key)
    except Exception as e:
        print("Error adding item: %s" % e)


def get_item(data):
    try:
        with db.cursor() as cursor:
            sql = "SELECT `item` FROM `shop` WHERE `item`=%s AND `price`=%s"
            for key, value in data.items():
                cursor.execute(sql, (key, value))
                result = cursor.fetchone()
                if not result:
                    print("Item does not exist: %s" % key)
                else:
                    return result
    except Exception as e:
        print("Error looking up item %s.\n%s" % (key, e))


def display_shop():
    try:
        with db.cursor() as cursor:
            sql = "SELECT `id` AS ID, `item` AS Item, `price` AS Price FROM `shop`"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print("Error looking up item.\n%s" % e)


def add_to_inventory(member, item):
    with db.cursor() as cursor:
        try:
            sql = "SELECT `inventory_slot_one` FROM `players` WHERE user_id=%s"
            cursor.execute(sql, member.id)
            result = cursor.fetchone()
            if result['inventory_slot_one'] is None:
                sql = "UPDATE players SET inventory_slot_one=%s WHERE user_id=%s"
                cursor.execute(sql, (item, member.id))
                db.commit()
            else:
                sql = "SELECT `inventory_slot_two` FROM `players` WHERE user_id=%s"
                cursor.execute(sql, member.id)
                result = cursor.fetchone()
                if result['inventory_slot_two'] is None:
                    sql = "UPDATE players SET inventory_slot_two=%s WHERE user_id=%s"
                    cursor.execute(sql, (item, member.id))
                    db.commit()
                else:
                    sql = "SELECT `inventory_slot_three` FROM `players` WHERE user_id=%s"
                    cursor.execute(sql, member.id)
                    result = cursor.fetchone()
                    if result['inventory_slot_three'] is None:
                        sql = "UPDATE players SET inventory_slot_three=%s WHERE user_id=%s"
                        cursor.execute(sql, (item, member.id))
                        db.commit()
                    else:
                        sql = "SELECT `inventory_slot_four` FROM `players` WHERE user_id=%s"
                        cursor.execute(sql, member.id)
                        result = cursor.fetchone()
                        if result['inventory_slot_four'] is None:
                            sql = "UPDATE players SET inventory_slot_four=%s WHERE user_id=%s"
                            cursor.execute(sql, (item, member.id))
                            db.commit()
        except Exception as e:
            print("[-] Error updating inventory for %s; %s" % (member.id, e))


def empty_inventory(member, slot):
    with db.cursor() as cursor:
        try:
            if slot == 1:
                sql = "UPDATE players SET inventory_slot_one= NULL WHERE user_id=%s"
                cursor.execute(sql, member.id)
                db.commit()
            if slot == 2:
                sql = "UPDATE players SET inventory_slot_two= NULL WHERE user_id=%s"
                cursor.execute(sql, member.id)
                db.commit()
            if slot == 3:
                sql = "UPDATE players SET inventory_slot_three= NULL WHERE user_id=%s"
                cursor.execute(sql, member.id)
                db.commit()
            if slot == 4:
                sql = "UPDATE players SET inventory_slot_four= NULL WHERE user_id=%s"
                cursor.execute(sql, member.id)
                db.commit()
        except Exception as e:
            print("[-] Error updating bank account for %s; %s" % (member.id, e))


def add_all_worry(data):
    for item in data:
        add_worry(item)


def add_worry(data):
    if get_worry(data):
        return
    try:
        with db.cursor() as cursor:
            for key, value in data.items():
                sql = "INSERT INTO `craft_table` (`worry`, `item_one`, `item_two`)" + \
                      " VALUES (%s, %s, %s)"
                cursor.execute(sql, (key, value[0], value[1]))
            db.commit()
            print("Added item %s to database." % data)
    except Exception as e:
        print("Error adding item: %s" % e)


def get_worry(data):
    try:
        with db.cursor() as cursor:
            for key, value in data.items():
                sql = "SELECT `worry` FROM `craft_table` WHERE `worry`=%s AND `item_one`=%s AND `item_two`=%s"
                cursor.execute(sql, (key, value[0], value[1]))
                result = cursor.fetchone()
                if not result:
                    print("Item does not exist: %s" % key)
                else:
                    return result
    except Exception as e:
        print("Error looking up item %s.\n%s" % (key, e))


def display_worry():
    try:
        with db.cursor() as cursor:
            sql = "SELECT `id` AS ID, `worry` AS Worry, `item_one` AS Item1, `item_two` AS Item2 FROM `craft_table`"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print("Error looking up item.\n%s" % e)

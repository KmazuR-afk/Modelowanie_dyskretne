import db_con


class Environment:
    def __init__(self,map_mat,conn,hunters=None,escapees=None,exits=None):
        self.map = map_mat
        self.hunters = hunters
        self.escapees = escapees
        self.exits = exits
        self.conn = conn

    def move_hunter(self,hunter):
        if not self.escapees:
            return

        closest_escapee = min(self.escapees,key=lambda escp: abs(hunter.pos_x - escp.pos_x) + abs(hunter.pos_y - escp.pos_y))
        decision = hunter.make_decision((closest_escapee.pos_x, closest_escapee.pos_y))
        old_x, old_y = hunter.pos_x, hunter.pos_y
        hunter.move(decision, self.map)
        self.map[old_y][old_x] = 0  # Zmień poprzednią pozycję na WHITE
        self.map[hunter.pos_y][hunter.pos_x] = 3

    def move_escape(self,escape):
        old_x, old_y = escape.pos_x, escape.pos_y
        possible_actions=[0,1,2,3]
        escape.step(self.hunters,self.exits, possible_actions)

        self.map[old_y][old_x]=0
        self.map[escape.pos_y][escape.pos_x]=2

    def check_captures(self):
        for escape in self.escapees:
            for hunter in self.hunters:
                if escape.pos_x==hunter.pos_x and escape.pos_y==hunter.pos_y:
                    print(f"Escape {escape.escapee_id} was caught by Hunter{hunter.id}!")
                    db_con.save_q_table(self.conn,escape.q_table,escape.escapee_id)
                    k_x=escape.pos_x
                    k_y=escape.pos_y
                    self.escapees.remove(escape)
                    self.map[k_y][k_x]=3
                    break

    def check_exits(self):
        for escape in self.escapees:
            if (escape.pos_x,escape.pos_y) in self.exits:
                print(f"Escape {escape.escapee_id} has fled!")
                db_con.save_q_table(self.conn,escape.q_table,escape.escapee_id)
                k_x = escape.pos_x
                k_y = escape.pos_y
                self.escapees.remove(escape)
                self.map[k_y][k_x] = 5
                break

    def step(self):

        for escapee in self.escapees:
            self.move_escape(escapee)
            for hunter in self.hunters:
                self.move_hunter(hunter)
        self.check_captures()
        self.check_exits()
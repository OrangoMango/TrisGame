from tkinter import *
from tkinter import messagebox
import random, time

class GridFrame:
	def __init__(self, game):
		self.game = game
		self.frame = Frame(game.tk, bd=1)
		self.id = Label(self.frame, text="    ", font="Calibri 20 bold", relief="solid")
		self.id.bind("<Button-1>", self.onclick)
		self.id.pack()
	def grid(self, **kwargs):
		try:
			self.x, self.y = kwargs["row"], kwargs["column"] #save grid coordinates
		except:
			self.x, self.y = 0, 0
		self.frame.grid(kwargs)
	def onclick(self, event):
		#print("Onclick")
		self.game.set_symbol(self.x, self.y, self.game.active_player)

class Game:
	def __init__(self, data):
		self.t1 = time.time()
		self.gameIsRunning = True
		self.ai = data[2]
		self.playernames = [data[0],data[1]]
		#print(self.playernames)
		self.tk = Tk()
		self.tk.title("Tris Game")
		self.tk.geometry("400x200")
		self.actualgame = [0] * 9 #actual game progress (1 -> x 2 -> o)
		self.active_player = 1
		self.grids = []
		for y in range(3):
			for x in range(3):
				f = GridFrame(self)
				f.grid(column=y, row=x)
				self.grids.append(f)
		self.plabel = Label(self.tk, text="Actual player: {0}".format(self.playernames[self.active_player-1]), font="Calibri 20 bold")
		self.plabel.place(x=0, y=120, anchor="nw")
		self.timel = Label(self.tk, text="{0:.2f}sec".format(time.time()-self.t1), fg="red", font="Calibri 20 bold")
		self.timel.place(x=0, y=165, anchor="nw")
		if data[3] == 2 and self.ai: # If AI is first the AI will place
			self.place_ai()
	def mainloop(self):
		while True:
			if self.gameIsRunning:
				self.timel.config(text="{0:.2f}sec".format(time.time()-self.t1))
				self.tk.update()
				time.sleep(0.04)
			else:
				self.ntime = time.time()-self.t1
				break
	def next_player(self):
		self.active_player = 2 if self.active_player == 1 else 1 #set the next player
		self.plabel.config(text="Actual player: {0}".format(self.playernames[self.active_player-1])) #update label
		self.tk.update()
	def check_grid(self, x, y):
		pos = y*3+x
		return self.actualgame[pos] #returns the item value in self.actualgame using x and y pos
	def victory(self, pn): #check is victory is possible
		list = self.actualgame
		if (list[0:3] == [pn, pn, pn]) or (list[3:6] == [pn, pn, pn]) or (list[6:9] == [pn, pn, pn]):
			return True
		for x in range(3):
			if (list[x] == pn) and (list[x+3] == pn) and (list[x+6] == pn):
				return True
		if (list[0] == pn) and (list[4] == pn) and (list[8] == pn):
			return True
		if (list[2] == pn) and (list[4] == pn) and (list[6] == pn):
			return True
		return False
	def random_set(self): #get a random index of self.actualgame
		empty = [x for x in range(9) if self.actualgame[x] == 0]
		return random.choice(empty)
	def set_from_number(self, n, playern): #set symbol from a index
		y = n // 3
		x = n % 3
		self.grids[n].id.config(text="O" if playern == 1 else "X")
		self.tk.update()
		self.tk.update_idletasks()
		self.actualgame[n] = playern
	def set_on_random_corner(self):
		empty_corners = []
		if self.actualgame[0] == 0:
			empty_corners.append(0)
		if self.actualgame[2] == 0:
			empty_corners.append(2)
		if self.actualgame[6] == 0:
			empty_corners.append(6)
		if self.actualgame[8] == 0:
			empty_corners.append(8)
		if empty_corners == []:
			return None
		return random.choice(empty_corners)
	def ai_insert(self): #AI
		if self.actualgame[4] == 0: # Place symbol on center if possible
			return 4;
		elif not (self.set_on_random_corner() is None): # Place symbol on a corner if possible
			return self.set_on_random_corner()
		empty = [x for x in range(9) if self.actualgame[x] == 0]
		emn = len(empty)
		backup = self.actualgame[:]
		for x in range(emn): #check if victory is possible
			self.actualgame = backup[:]
			self.actualgame[empty[x]] = 2
			if self.victory(2): #if victory
				self.actualgame = backup[:]
				return empty[x] #return the index
		for x in range(emn): #if there is no victory, make possible that computer can not lose
			self.actualgame = backup[:]
			self.actualgame[empty[x]] = 1
			if self.victory(1): #if the player can win
				self.actualgame = backup[:]
				return empty[x] #return player index
		self.actualgame = backup[:]
		return self.random_set() #if there are no possibilities, return a random index
	def no_insert(self):
		return not (0 in self.actualgame) #if the board is full
	def quit(self):
		self.tk.destroy()
	def set_symbol(self, x, y, playern):
		if self.check_grid(x, y) == 0: #You can only place symbols if the frame doesn't contain another symbol
			pos = y*3+x
			self.grids[pos].id.config(text="O" if playern == 1 else "X")
			self.tk.update()
			self.tk.update_idletasks()
			self.actualgame[pos] = playern
			if self.victory(self.active_player): #if victory
				self.gameIsRunning = False
				messagebox.showinfo("Game Over", "{0} won the game".format(self.playernames[self.active_player-1]))
				self.quit()
			elif self.no_insert(): #if the board is full
				self.gameIsRunning = False
				messagebox.showinfo("Game Over", "Game has finished, no winner")
				self.quit()
			else:
				if not self.ai:
					self.next_player()
				elif self.ai == True:
					self.place_ai()
				else:
					raise Exception('No ai is active')
	def place_ai(self):
		self.next_player()
		self.plabel.config(text="Actual player: {0}".format(self.playernames[self.active_player-1])) #update label
		self.tk.update()
		time.sleep(0.5)
		self.set_from_number(self.ai_insert(), 2)
		if self.victory(self.active_player):
			self.gameIsRunning = False
			messagebox.showinfo("Game Over", "AI won the game")
			self.quit()
		elif self.no_insert():
			self.gameIsRunning = False
			messagebox.showinfo("Game Over", "Game has finished, no winner")
			self.quit()
		else:
			self.next_player()
			self.plabel.config(text="Actual player: {0}".format(self.playernames[self.active_player-1])) #update label
			self.tk.update()

class Setup:
	def __init__(self):
		self.tk = Tk()
		self.tk.title("Tris setup wizard")
		self.infoboxes = []
		self.txtvar = StringVar()
		for x in range(2):
			l = Label(self.tk, text="Player{0} name:".format(x+1))
			l.grid(column=0, row=x)
			e = Entry()
			e.grid(column=1, row=x)
			self.infoboxes.append((l,e))
		self.infoboxes[1][1].config(textvariable=self.txtvar)
		self.odata = ""
		def ck():
			if self.infoboxes[1][1]['state'] == 'normal':
				self.infoboxes[1][1]['state'] = "disable"
				self.odata = self.txtvar.get()
				self.txtvar.set("AI")
			else:
				self.infoboxes[1][1]['state'] = "normal"
				self.txtvar.set(self.odata)
		self.aivar = IntVar()
		self.ck = Checkbutton(self.tk, text="Against AI", variable=self.aivar, command=ck)
		self.ck.grid(row=2, column=0, columnspan=2)
		stl = Label(self.tk, text="Who starts?")
		stl.grid(row=3, column=0)
		self.whostarts = IntVar()
		self.whostarts.set(1)
		r1 = Radiobutton(self.tk, text="Player1", value=1, variable=self.whostarts)
		r2 = Radiobutton(self.tk, text="Player2", value=2, variable=self.whostarts)
		r1.grid(row=4, column=0)
		r2.grid(row=4, column=1)
		okb = Button(self.tk, text="Save data", command=self.ok)
		okb.grid(row=5, column=3)
		self.start = False
	def ok(self):
		#print(self.whostarts.get())
		self.results = [self.infoboxes[0][1].get(), self.infoboxes[1][1].get(), bool(self.aivar.get()), self.whostarts.get()]
		if "" in self.results:
			messagebox.showerror("Invalid input", "Invalid name given")
			return
		self.start = True

if __name__ == '__main__':
	s = Setup()
	while not s.start: #setup loop
		time.sleep(0.01)
		s.tk.update()
	s.tk.destroy()
	data = s.results
	g = Game(data)
	g.mainloop()

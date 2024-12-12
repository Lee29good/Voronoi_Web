# $LAN=Python$
# Author : 李明儒 Ming-Ru Li
# Student ID : M133040055
# Date : 2024/12/4

import tkinter as tk
from tkinter import font , ttk , filedialog , messagebox
import random 
import math

class VoronoiDiagram:
  # 創建主視窗,設定視窗大小,設定視窗標題
  def __init__(self, root):
    self.root = root
    self.root.geometry("1200x800")
    self.root.title("Voronoi Diagram")
    self.root.configure(bg="lightgray")
    
    # 字體設置
    self.custom_font = font.Font(family="Helvetica", size=20, weight="bold")
    self.custom_font2 = font.Font(family="Helvetica", size=13, weight="bold")
    self.title_font = font.Font(family="'Helvetica'", size=60, weight="bold", slant="italic")
    
    # 創建畫布和功能區域
    self.create_canvas_area()
    self.create_setting_area()

    #滑鼠事件綁定
    self.is_mouse_pressed = False
    self.canvas.bind("<ButtonPress-1>", self.on_canvas_press)
    self.canvas.bind("<Motion>", self.on_canvas_move)
    self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release) 

    # voronoi diagram相關結構
    self.point_index = 0 
    self.current_data_index = 0
    self.points = []
    self.edges = [] 
    self.edges_canvas = []
    self.data_sets = []
    self.execute_valid = True
    self.isDoingStepbyStep = False
    
  def create_canvas_area(self):
    # 畫布跟標題區域
    canva_area = tk.Frame(self.root, width=620, height=700, borderwidth=2, relief="solid")
    canva_area.grid(row=0, column=0, padx=(25, 0), pady=(50, 25))

    title = tk.Label(canva_area, text="Voronoi Diagram", fg="blue", font=self.title_font)
    title.grid(row=0, column=0, sticky='w')

    #畫布區(600x600)
    self.canvas = tk.Canvas(canva_area, width=590, height=590, borderwidth=2, relief="solid")
    self.canvas.grid(row=1, column=0, sticky='nsew')

  def create_setting_area(self):
    # 功能區域(在右側)
    setting_area = tk.Frame(self.root, width=500, height=700, bg="white")
    setting_area.grid(row=0, column=1, padx=25, pady=(50, 25))
    setting_area.grid_propagate(False)

    # 創建四個功能性區塊
    self.create_vertex_settings(setting_area)
    self.create_operation_settings(setting_area)
    self.create_vertex_record(setting_area)
    self.create_line_record(setting_area)
    
  def create_vertex_settings(self, parent):
    # 點操作區域
    setting1 = tk.Frame(parent, width=230, height=340)
    setting1.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
    setting1.grid_propagate(False)

    vertex_frame = tk.Frame(setting1, width=230, height=340)
    vertex_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    vertex_title = tk.Label(vertex_frame, text="<點操作>", fg="blue", font=self.custom_font)
    vertex_title.grid(row=0, columnspan=2, sticky='w')

    self.vertex_position_label = tk.Label(vertex_frame, text="滑鼠位置:", fg="black", font=self.custom_font)
    self.vertex_position_label.grid(row=1, column=0, pady=(20, 0), sticky='w')
    self.vertex_position_value = tk.Label(vertex_frame, text="(X,Y)", fg="black", font=self.custom_font)
    self.vertex_position_value.grid(row=1, column=1, padx=(10,0), pady=(20, 0))

    self.vertex_x_input = self.create_input(vertex_frame, "X(0~600):", 2)
    self.vertex_y_input = self.create_input(vertex_frame, "Y(0~600):", 3)

    add_vertex_button = tk.Button(vertex_frame, text="添加點", bg="lightblue", fg="black", font=self.custom_font2, width=7, command=self.add_vertex)
    add_vertex_button.grid(row=4, columnspan=2, sticky='w')

    self.create_random_vertex_section(vertex_frame)
    
  def create_random_vertex_section(self, parent):
    vertex_random_title = tk.Label(parent, text="~隨機生成點~", fg="blue", font=self.custom_font)
    vertex_random_title.grid(row=5, columnspan=2, pady=(30, 0), sticky='w')

    random_amount_label = tk.Label(parent, text="生成數量:", fg="black", font=self.custom_font)
    random_amount_label.grid(row=6, column=0, sticky='w')
    self.random_amount_input = tk.Entry(parent, width=7)
    self.random_amount_input.grid(row=6, column=1,sticky="w")

    random_button = tk.Button(parent, text="隨機產生", bg="lightblue", fg="black", font=self.custom_font2, width=7, command=self.generate_random_vertices)
    random_button.grid(row=7, columnspan=2, sticky='w')

  def create_input(self, parent, label_text, row):
    label = tk.Label(parent, text=label_text, fg="black", font=self.custom_font)
    label.grid(row=row, column=0, sticky='w')
    entry = tk.Entry(parent, width=7)
    entry.grid(row=row, column=1, sticky="w")
    return entry
  
  def create_operation_settings(self, parent):
    # 執行與檔案區域
    setting2 = tk.Frame(parent, width=230, height=340)
    setting2.grid(row=0, column=1, padx=10, pady=5, sticky='nsew')
    setting2.grid_propagate(False)

    operate_frame = tk.Frame(setting2, width=230, height=150)
    operate_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    operate_title = tk.Label(operate_frame, text="<動作>", fg="blue", font=self.custom_font)
    operate_title.grid(row=0, sticky='w')

    self.create_operation_buttons(operate_frame)

    file_frame = tk.Frame(setting2, width=230, height=150)
    file_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
    file_title = tk.Label(file_frame, text="<檔案>", fg="blue", font=self.custom_font)
    file_title.grid(row=0, sticky='w')

    self.create_file_buttons(file_frame)

  def create_operation_buttons(self, parent):
    buttons = [
      ("執行", self.execute_action),
      ("下一組資料", self.next_data_set),
      ("一步一步執行", self.step_by_step),
      ("清空頁面", self.clear_canvas)
    ]
    for i, (text, command) in enumerate(buttons):
      button = tk.Button(parent, text=text, bg="lightblue", fg="black", font=self.custom_font2, width=13, command=command)
      button.grid(row=i + 1, padx=(25, 0), pady=5)

  def create_file_buttons(self, parent):
    buttons = [
      ("讀取輸入檔", self.load_input_file),
      ("讀取輸出檔", self.load_output_file),
      ("輸出文字檔", self.export_text_file)
    ]
    for i, (text, command) in enumerate(buttons):
      button = tk.Button(parent, text=text, bg="lightblue", fg="black", font=self.custom_font2, width=13, command=command)
      button.grid(row=i + 1, padx=(25, 0), pady=5)

  def create_vertex_record(self, parent):
    # 點資料區域
    setting3 = tk.Frame(parent, width=230, height=340)
    setting3.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
    setting3.grid_propagate(False)

    self.vertex_info_label = tk.Label(setting3, text="<點資料>  0個點", fg="blue", font=self.custom_font)
    self.vertex_info_label.grid(row=0, sticky='w')

    self.vertex_record = ttk.Treeview(setting3, columns=("index", "x_column", "y_column"), show='headings', height=15)
    self.vertex_record.heading("index", text="index")
    self.vertex_record.heading("x_column", text="X")
    self.vertex_record.heading("y_column", text="Y")
    self.vertex_record.column("index", width=70)
    self.vertex_record.column("x_column", width=70)
    self.vertex_record.column("y_column", width=70)
    self.vertex_record.grid(row=1, padx=7)

  def create_line_record(self, parent):
    # 邊資料區域
    setting4 = tk.Frame(parent, width=230, height=340)
    setting4.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
    setting4.grid_propagate(False)

    label4 = tk.Label(setting4, text="<邊資料>", fg="blue", font=self.custom_font)
    label4.grid(row=0, sticky='w')

    self.line_record = ttk.Treeview(setting4, columns=("start", "end"), show='headings', height=15)
    self.line_record.heading("start", text="Start")
    self.line_record.heading("end", text="End")
    self.line_record.column("start", width=100)
    self.line_record.column("end", width=100)
    self.line_record.grid(row=1, padx=7)

  ##Canva畫布中的滑鼠事件
  def on_canvas_press(self, event):
    self.is_mouse_pressed = True  # 設置按下狀態
    self.update_coordinates(event.x, event.y)

  def on_canvas_move(self, event):
    if self.is_mouse_pressed:  # 只有在按下時才更新坐標
      self.update_coordinates(event.x, event.y)
      
  def on_canvas_release(self, event):
    self.is_mouse_pressed = False  # 重置按下狀態並固定坐標
    x, y = event.x, event.y
    self.vertex_position_value.config(text=f"({x},{y})")

    # 刪除畫布上標記為 "point" 的所有圓點
    self.canvas.delete("point")
    # 在畫布上繪製一個小圓點 , 顯示座標
    self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="red", outline="black", tags="point")
    self.canvas.create_text(x + 10, y, text=f"({x},{y})", anchor="nw", fill="black" , tags="point")

  def update_coordinates(self, x, y):  
    # 檢查坐標是否在範圍內
    if 0 <= x <= 600 and 0 <= y <= 600:
      # 隨著畫布滑鼠移動，數值的更新
      self.vertex_position_value.config(text=f"({x},{y})")
      self.vertex_x_input.delete(0, tk.END)
      self.vertex_x_input.insert(0, str(x))
      self.vertex_y_input.delete(0, tk.END)
      self.vertex_y_input.insert(0, str(y))

  ##點處理(新增、隨機生成、排序treeview)
  def add_vertex(self):
    try:
      x = int(self.vertex_x_input.get())
      y = int(self.vertex_y_input.get())
      if 0 <= x <= 600 and 0 <= y <= 600:
        if (x,y) not in self.points: 
          self.point_index += 1
          self.vertex_record.insert("", "end", values=(self.point_index, x, y))
          self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")
          self.vertex_info_label.config(text=f"<點資料>  {self.point_index}個點")
          self.points.append((x,y))
          # 按照字典序排序
          self.points = sorted(self.points)
          self.vertex_treeview_lexicalorder()
          # 在畫布上面也標上座標(方便觀察)
          self.canvas.create_text(x + 10, y, text=f"({x},{y})", anchor="nw", fill="black")
          
        # 清空輸入框方便輸入下一個點
        self.vertex_x_input.delete(0, 'end')
        self.vertex_y_input.delete(0, 'end')
      else:
        self.show_error("坐標必須在(0, 0)到(600, 600)之間。")
    except ValueError:
      self.show_error("請輸入有效的整數坐標。")

  def generate_random_vertices(self):
    try:
      count = int(self.random_amount_input.get())
      if count > 0:
        for _ in range(count):
          x = random.randint(0, 600)
          y = random.randint(0, 600)
          self.add_vertex_to_treeview(x, y)
          self.points.append((x,y))
        
        self.points = sorted(self.points)  
        
        self.vertex_treeview_lexicalorder()
      else:
        self.show_error("請輸入一個正整數。")
    except ValueError:
      self.show_error("請輸入有效的整數。")

  def add_vertex_to_treeview(self, x, y):
    self.point_index += 1
    self.vertex_record.insert("", "end", values=(self.point_index, x, y))
    # 在畫布上面也標上點跟座標(方便觀察)
    self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")
    text_id = self.canvas.create_text(x + 10, y, text=f"({x},{y})", anchor="nw", fill="black")
    # 更新點數量
    self.vertex_info_label.config(text=f"<點資料>  {self.point_index}個點")
    
  def vertex_treeview_lexicalorder(self):
    self.vertex_record.delete(*self.vertex_record.get_children())
    temp_index = 1
    for point in self.points:
      x , y = point
      self.vertex_record.insert("", "end", values=(temp_index, x, y))
      temp_index += 1
    
  def show_error(self, message):
    error_window = tk.Toplevel(self.root)
    error_window.title("錯誤")
    tk.Label(error_window, text=message, fg="red").pack(padx=20, pady=20)
    tk.Button(error_window, text="關閉", command=error_window.destroy).pack(pady=10)

  # 跑 Voronoi algorithm 產出結果
  def execute_action(self):
    run()
    if(self.execute_valid):
      new_diagram = Diagram(self.points)
      new_diagram.divide()
      self.execute_valid = False
    global running
    running = False
    
  def Voronoi_diagram_function(self):
    self.VD_InThreeNode()

  def next_data_set(self):

    # 確保有資料集可以讀取
    if self.current_data_index < len(self.data_sets):
      
      self.clear_canvas()
      # 加載當前資料集到 self.points 中
      self.points = self.data_sets[self.current_data_index]
      
      # 將點繪製到畫布上
      for point in self.points:
        x,y = point
        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")  # 調整大小和顏色
        self.add_vertex_to_treeview(x, y)
        
        
      self.current_data_index += 1
      self.points = sorted(self.points)  
      self.vertex_treeview_lexicalorder()
      self.execute_valid = True
      self.isDoingStepbyStep = False
      global running 
      running = False
    else:
      self.show_error("已無更多資料可供讀取。")

  def step_by_step(self):    
     
    if(self.isDoingStepbyStep == False):
      new_diagram = Diagram(self.points)
      new_diagram.divide()
    else:
      next_step()
    self.isDoingStepbyStep = True

  def clear_canvas(self):
    self.canvas.delete("all")
    self.vertex_record.delete(*self.vertex_record.get_children())
    self.line_record.delete(*self.line_record.get_children())
    self.vertex_info_label.config(text="<點資料>  0個點")
    self.vertex_position_value.config(text="(X,Y)")
    self.point_index = 0
    self.points = []
    self.edges = []
    self.edges_canvas = []
    self.execute_valid = True
    self.isDoingStepbyStep = False

  def load_input_file(self):
    self.execute_valid = True
    # 做選擇file並且讀取檔案
    self.select_file()
    # 確認讀取資料

  def select_file(self):
    self.execute_valid = True
    # 使用文件對話框選取文件
    file_path = filedialog.askopenfilename(
      title="選擇測試資料文件",
      filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if file_path:
      self.read_file(file_path)
      
  def load_output_file(self):
    self.execute_valid = True
    self.load_output()

  # 輸出目前畫布資料文字檔
  def export_text_file(self):
    self.save_to_file()
      
  def VD_InThreeNode(self,color):
    if(len(self.points) ==0 ):
      print("Remind: 目前沒有任何的點")
      return 
    elif(len(self.points) == 1):
      print("Remind : 只有一個點!!")
    elif(len(self.points) == 2):
      x1,y1 = self.points[0]
      x2,y2 = self.points[1]
      if((x1 == x2) & (y1 == y2)):
        print("兩個是同一點")
        return
      self.draw_perpendicular_bisector(x1, y1, x2, y2,color)
    else:
      
      x1,y1 = self.points[0]
      x2,y2 = self.points[1]
      x3,y3 = self.points[2]
      
      # 標點
      for point in self.points:
        x , y = point
        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")
        self.canvas.create_text(x + 10, y, text=f"({x},{y})", anchor="nw", fill="black")
      
      # 如果三點共線
      if(self.are_points_collinear(self.points)):
        sorted_point = self.find_middle_point(self.points)
        p1, p2, p3 = sorted_point
        #提取點座標
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        
        self.draw_perpendicular_bisector(x1, y1, x2, y2,color)
        self.draw_perpendicular_bisector(x2, y2, x3, y3,color)
        return
      
      # 根據sorted point求外心 (Ux,Uy為外心值)
      sorted_points = self.sort_points_counterclockwise(self.points)
      Ux,Uy = self.circumcenter(sorted_points)
      
      # 根據排序好的points求順時針的法向量 , 並且由外心進行延伸
      norm1 = self.normal_vector(sorted_points[0], sorted_points[1])
      norm2 = self.normal_vector(sorted_points[1], sorted_points[2])
      norm3 = self.normal_vector(sorted_points[2], sorted_points[0])
      
      # 計算法向量的終點，這裡使用一個長度（例如100）來繪製法向量
      line_length = 1000000
    
      # 將外心和法向量結合，進行延伸繪製射線
      self.canvas.create_line(Ux, Uy, Ux + norm1[0] * line_length, Uy + norm1[1] * line_length, fill=color)
      self.canvas.create_line(Ux, Uy, Ux + norm2[0] * line_length, Uy + norm2[1] * line_length, fill=color)
      self.canvas.create_line(Ux, Uy, Ux + norm3[0] * line_length, Uy + norm3[1] * line_length, fill=color)

      # 將畫布內線段距離記錄下來
      self.record_line(Ux, Uy, Ux + norm1[0] * line_length, Uy + norm1[1] * line_length, sorted_points[0], sorted_points[1])
      self.record_line(Ux, Uy, Ux + norm2[0] * line_length, Uy + norm2[1] * line_length, sorted_points[1], sorted_points[2])
      self.record_line(Ux, Uy, Ux + norm3[0] * line_length, Uy + norm3[1] * line_length, sorted_points[2], sorted_points[0])
      
  # test 將點以逆時針排序，為了求法向量
  def sort_points_counterclockwise(self,points):
    # 假設 points 是 [(x1, y1), (x2, y2), (x3, y3)]
    p1, p2, p3 = points
    
    # 提取點的坐標
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    
    # 計算叉積來確定方向
    cross_product = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    
    # 如果叉積，表示三点共線
    if cross_product == 0:
      print("The points are collinear.")
    
    # 如果叉積為負(因為y座標倒轉)，表示 points 已經是逆時針方向
    if cross_product < 0:
      return points  # 直接返回原來的順序
    
    # 如果叉積為負，表示 points 是順時針方向，交換最後兩個點以獲得逆時針方向
    return [p1, p3, p2]
  
  # 求外心公式
  def circumcenter(self,points):
    (x1, y1), (x2, y2), (x3, y3) = points
    # 外心公式會用到
    D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    
    if D == 0:
      raise ValueError("三個點共線，無法確定外心")
    
    # 計算外心坐標
    Ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / D
    Uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / D
    
    return (Ux, Uy)
  
  def normal_vector(self, point1, point2):
    # 提取點的座標
    x1, y1 = point1
    x2, y2 = point2
    
    # 計算向量 AB 的分量
    dx = x2 - x1
    dy = y2 - y1
    
    # 計算向量的長度
    length = math.hypot(dx, dy)
    
    # 確保向量長度不為零，避免除以零的情況
    if length == 0:
        raise ValueError("兩點相同，無法計算法向量")
    
    # 計算單位法向量
    unit_normal = (-dy / length, dx / length)  # 順時針方向的單位法向量
    return unit_normal
    
  def record_line(self, px1, py1, px2, py2, parent1, parent2):
    # 先加入邊的行列, 並且先記錄在edge陣列中
    edge = ((px1, py1), (px2, py2), parent1, parent2)
    if edge not in self.edges:
      self.edges.append(edge)
    
    px1, py1, px2, py2 = self.clip_to_bounds(px1, py1, px2, py2)

    px1, py1, px2, py2 = int(px1) , int(py1) , int(px2), int(py2)
    
    # 將線段記錄下來
    edge = ((px1, py1), (px2, py2))
    # note : px1 < px2 , if(px1 < px2) py1 <=py2
    if px1 > px2 or (px1 == px2 and py1 > py2):
        (px1, py1), (px2, py2) = (px2, py2), (px1, py1)
      
    edge = ((px1, py1), (px2, py2))
    
    if((px1 == px2) & (py1==py2)):
      return
    
    if edge not in self.edges_canvas:
      self.edges_canvas.append(edge)
      
    # 排序邊，根據每條邊的兩個點按字典順序
    self.edges.sort(key=lambda edge: (min(edge[0], edge[1]), max(edge[0], edge[1])))
    self.edges_canvas.sort(key=lambda edge: (min(edge[0], edge[1]), max(edge[0], edge[1])))
    self.line_treeview_lexicalorder()

  def line_treeview_lexicalorder(self):
    self.line_record.delete(*self.line_record.get_children())
    for edge in self.edges_canvas :
      (x1, y1), (x2, y2) = edge
      edge_start = f"({x1}, {y1})"
      edge_end = f"({x2}, {y2})"
      self.line_record.insert("", "end", values=(edge_start,edge_end))
      
  def draw_perpendicular_bisector(self, x1, y1, x2, y2,color):
    
    # 計算中點座標
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    # perpendicular_bisector 的計算
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    # 垂直單位向量
    ux, uy = -dy / length, dx / length
    # 設定中垂線長度
    line_length = 1000000
    # 計算中垂線起點和終點
    px1 = mid_x + ux * line_length
    py1 = mid_y + uy * line_length
    px2 = mid_x - ux * line_length
    py2 = mid_y - uy * line_length 
    
    parent1 = (x1,y1)
    parent2 = (x2,y2)
    
    self.record_line(px1, py1, px2, py2, parent1, parent2)
    
    # 繪製中垂線
    self.canvas.create_line(px1, py1, px2, py2, fill=color)
    
  def cal_perpendicular_bisector(self, x1, y1, x2, y2):
    
    # 計算中點座標
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    # perpendicular_bisector 的計算
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    # 垂直單位向量
    ux, uy = -dy / length, dx / length
    # 設定中垂線長度
    line_length = 1000000
    # 計算中垂線起點和終點
    px1 = mid_x + ux * line_length
    py1 = mid_y + uy * line_length
    px2 = mid_x - ux * line_length
    py2 = mid_y - uy * line_length 
    
    return (px1, py1, px2, py2)
    
  def are_points_collinear(self, points):
    p1, p2, p3 = points
    
    # 提取點座標
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    
    # 計算cross
    cross_product = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

    # cross 為零則三點共線
    return cross_product == 0
  
  def find_middle_point(self, points):
    p1, p2, p3 = points
    
    # 提取點的座標
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    
    # 判斷點p2是否在p1 和 p3 中間
    if (min(x1, x3) <= x2 <= max(x1, x3)) and (min(y1, y3) <= y2 <= max(y1, y3)):
        return (p1,p2,p3)  # p2 在中間
    # 判斷點p3是否在p1 和 p2 中間
    elif (min(x1, x2) <= x3 <= max(x1, x2)) and (min(y1, y2) <= y3 <= max(y1, y2)):
        return (p1,p3,p2)  # p3 在中間
    # 如果都不在中間，則返回 p1
    return (p2,p1,p3)  # p1 在中間
  
  # 只截取到畫布上的邊
  def clip_to_bounds(self ,x1, y1, x2, y2):
    # 定義邊界 , 只截到邊界上的點
    min_x, max_x = 0, 600
    min_y, max_y = 0, 600
    if x1 < min_x:
      y1 += (min_x - x1) * (y2 - y1) / (x2 - x1)
      x1 = min_x
    elif x1 > max_x:
      y1 += (max_x - x1) * (y2 - y1) / (x2 - x1)
      x1 = max_x

    if x2 < min_x:
      y2 += (min_x - x2) * (y1 - y2) / (x1 - x2)
      x2 = min_x
    elif x2 > max_x:
      y2 += (max_x - x2) * (y1 - y2) / (x1 - x2)
      x2 = max_x

    if y1 < min_y:
      x1 += (min_y - y1) * (x2 - x1) / (y2 - y1)
      y1 = min_y
    elif y1 > max_y:
      x1 += (max_y - y1) * (x2 - x1) / (y2 - y1)
      y1 = max_y

    if y2 < min_y:
      x2 += (min_y - y2) * (x1 - x2) / (y1 - y2)
      y2 = min_y
    elif y2 > max_y:
      x2 += (max_y - y2) * (x1 - x2) / (y1 - y2)
      y2 = max_y

    return x1, y1, x2, y2
  
  def read_file(self, file_path):
    self.current_data_index = 0
    self.data_sets = []  # 用於儲存所有測試資料
    with open(file_path, 'r', encoding='utf-8') as file:
      current_data = []  # 當前測試資料組的點陣列
      n = 0
      reading_points = False

      for line in file:
        line = line.strip()
        if line.startswith("#") or line == "":
          continue  # 忽略註解和空行

        # 嘗試解析為點數或座標
        if not reading_points:  # 如果尚未設定點數，則嘗試讀取點數
          try:
            n = int(line)
            if n == 0:
              break
            current_data = []  # 初始化新的一組測試資料
            reading_points = True  # 開始讀取座標點
          except ValueError:
            continue
        else:
          # 讀取 n 個點並加入當前的點陣列
          try:
            x, y = map(int, line.split())
            if (x,y) not in current_data:
              current_data.append((x, y))
            n -= 1
            if n == 0:  # 完成當前組的點讀取
              self.data_sets.append(current_data)  # 將完整的一組資料儲存
              reading_points = False
          except ValueError:
            continue
    
    self.next_data_set()
  
  # 輸出文字檔案功能
  def save_to_file(self):
    # 彈出視窗，讓使用者選擇儲存檔案的名稱和路徑
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    # 如果使用者取消選擇，file_path 會是空字串
    if not file_path:
      return

    try:
      with open(file_path, 'w') as file:
        # 寫入每個點的座標
        for point in self.points:
          x, y = point
          file.write(f"P {x} {y}\n")
        # 寫入每條邊的座標
        for edge in self.edges_canvas:
          e1, e2 = edge
          x1, y1 = e1
          x2, y2 = e2
          file.write(f"E {x1} {y1} {x2} {y2}\n")
        # 顯示成功訊息
        messagebox.showinfo("成功", f"資料已成功儲存至 {file_path}")
    except Exception as e:
      # 顯示錯誤訊息
      messagebox.showerror("錯誤", f"儲存檔案時發生錯誤：{e}")

  #讀取輸出檔
  def load_output(self):

    filename = filedialog.askopenfilename(title="Select Output File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))

    if not filename:
      return  # 如果沒有選擇檔案，則不執行後續操作

    self.clear_canvas()
    # 讀取輸入檔案
    with open(filename, 'r', encoding='utf-8') as file:
      lines = file.readlines()
    
    for line in lines:
      parts = line.strip().split()
      if parts[0] == 'P':
        # 點：格式 P x y
        x, y = int(parts[1]), int(parts[2])
        self.points.append((x, y))
        self.add_vertex_to_treeview(x,y)
        # 在畫布上繪製點
        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")
      elif parts[0] == 'E':
        # 邊：格式 E x1 y1 x2 y2
        x1, y1, x2, y2 = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]) 
        self.record_line(x1,y1,x2,y2)
        
    # 在畫布上繪製所有儲存在 self.edges 中的邊
    for edge in self.edges:
      (x1, y1), (x2, y2) = edge
      self.canvas.create_line(x1, y1, x2, y2, fill="green")  # 用綠色繪製邊
      
  # 在canvas上刪除邊操作
  def delete_line_by_endpoints(self,x1, y1, x2, y2):
    # 遍歷畫布中的所有物件
    for item in self.canvas.find_all():
        # 獲取物件的座標
        coords = self.canvas.coords(item)
        # 檢查是否與目標座標匹配
        if len(coords) == 4 and ((coords[0], coords[1], coords[2], coords[3]) == (x1, y1, x2, y2) or 
                                  (coords[0], coords[1], coords[2], coords[3]) == (x2, y2, x1, y1)):
          self.canvas.delete(item)
          break  
      
  # 在canvas上更改點跟邊顏色操作
  def change_node_and_edge_color(self,vertexSet,edgeSet,color):
    # 遍歷畫布中的所有物件
    for item in self.canvas.find_all():
      
      coords = self.canvas.coords(item)
      
      # 如果點再vertexSet中 -> 將點顏色改成color
      if len(coords) == 4:  # 這是點 (圓形) 的坐標，應該有四個座標
        x1, y1, x2, y2 = coords
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        if (center_x, center_y) in vertexSet:
          self.canvas.itemconfig(item, fill=color)

        edge = ((x1, y1), (x2, y2))
        for edges in edgeSet:
          if (edge[0] == edges[0] and edge[1] == edges[1]) or (edge[0] == edges[1] and edge[1] == edges[0]):
            self.canvas.itemconfig(item, fill=color)
  
  def delete_hull_edges(self, hull):
    """
    刪除畫布上由 hull 點形成的所有邊。
    
    :param hull: Convex Hull 的點順序列表 [(x1, y1), (x2, y2), ...]
    """
    if len(hull) < 2:
        return
    
    # 遍歷點集合並刪除對應邊
    for i in range(len(hull)):
        x1, y1 = hull[i]
        x2, y2 = hull[(i + 1) % len(hull)]  # 與下一點連接，最後一點與第一點閉合
        self.delete_line_by_endpoints(x1, y1, x2, y2)
        
  def clear_all_edges(self):
    #刪除所有邊canvas上的
    """
    清空 Canvas 上的所有線段（邊）。
    
    :param canvas: Tkinter 的 Canvas 元件
    """
    for item in self.canvas.find_all():
        # 確認物件類型是否為線段 (line)
        if self.canvas.type(item) == "line":
            self.canvas.delete(item)
            print(f"刪除線段: {self.canvas.coords(item)}")
    print("已清空 Canvas 上的所有邊")
    
  def create_edges(self,edgeSet):
    for edge in edgeSet:
      print("create:",(edge[0][0],edge[0][1],edge[1][0],edge[1][1]))
      app.canvas.create_line(edge[0][0],edge[0][1],edge[1][0],edge[1][1],fill="black")
      
  def clear_treeview(self):
    """
    清空 Treeview 的所有項目。
    
    :param treeview: Tkinter 的 Treeview 元件
    """
    for item in self.line_record.get_children():
      self.line_record.delete(item)
    print("Treeview 已清空")

##########第二個class diagram ####################################################################################################

class Diagram:
  def __init__(self , points) : 
    self.points = points
    self.edges = []
    
  #切一半
  def divide(self):
    print("\n\n開始做 voronoi diagram ============================================================================================================================================================================================\n")
    #大於三個點
    #先排序好順序
    self.sort_Points()
    
    if(len(self.points)>3):
      self.left_sub_diagram = Diagram(self.points[:len(self.points) // 2])
      self.right_sub_diagram = Diagram(self.points[len(self.points) // 2:])
      self.left_sub_diagram.divide()
      stop()
      self.right_sub_diagram.divide()
      stop()
      self.points = self.left_sub_diagram.points + self.right_sub_diagram.points
      self.edges = self.left_sub_diagram.edges + self.right_sub_diagram.edges
      app.clear_all_edges()
      app.create_edges(self.edges)
      app.change_node_and_edge_color(self.left_sub_diagram.points,self.left_sub_diagram.edges,"red")
      app.change_node_and_edge_color(self.right_sub_diagram.points,self.right_sub_diagram.edges,"blue")
      lefthull = self.left_sub_diagram.ConvexHull()
      righthull = self.right_sub_diagram.ConvexHull()
      self.left_sub_diagram.draw_hull(lefthull)
      self.right_sub_diagram.draw_hull(righthull)
      stop()
      app.delete_hull_edges(lefthull)
      app.delete_hull_edges(righthull)
      hull = self.ConvexHull()
      self.draw_hull(hull)
      return self.Merge()
    #小於等於三個點
    else:
      app.clear_all_edges()
      #丟points跟edges進去VD跑
      app.points = self.points[:]
      app.edges = self.edges[:]
      app.VD_InThreeNode("green")
      # app.VD 會 return 對應的edges回來
      self.edges = app.edges[:]
      app.edges = []
      app.points = []
      
  #排序點
  def sort_Points(self):
    # 假設 self.points 是一個二維點的列表
    # 根據 x 坐標排序
    self.points.sort(key=lambda point: point[0])
    
  #合併
  def Merge(self):
    # 1.將左右兩邊的點merge ,左右兩個子圖的邊merge
    print("\n>>>merge左右點<<<")
    print("$所有左邊點:",self.left_sub_diagram.points)
    print("$所有右邊點:",self.right_sub_diagram.points)
    print("$所有左邊邊:",self.left_sub_diagram.edges)
    print("$所有右邊邊:",self.right_sub_diagram.edges)
    
    # 2.如果不為共線，則可以先算出convex_Hull否則不算
    if self.is_collinear():
      #所有點共線相對於有左右兩邊的最近的兩個點去做bisector
      point1,point2 = self.find_closest_points_of_two_sets(self.left_sub_diagram.points,self.right_sub_diagram.points)
      (bisx1,bisy1,bisx2,bisy2) = app.cal_perpendicular_bisector(point1[0],point1[1],point2[0],point2[1])
      app.canvas.create_line(bisx1,bisy1,bisx2,bisy2,fill="orange")
      stop()
      self.edges.append(((bisx1,bisy1),(bisx2,bisy2),point1,point2))
      return
    else:
      hull = self.ConvexHull()
    
    # 3.算上下公切線
    upperTangent, lowerTangent = self.FindCommonTangent(hull,self.left_sub_diagram.points,self.right_sub_diagram.points)
    
    # 4.ConvexHull
    self.HyperPlane(upperTangent, lowerTangent)
    
    app.delete_hull_edges(hull)
    
    app.change_node_and_edge_color(self.points,self.edges,"green")
    stop()    
    
    # 清空line_record 的 treeview 再重新加入
    app.clear_treeview()
    app.edges = []
    app.edges_canvas = []
    for edge in self.edges:
      try:
          app.record_line(edge[0][0], edge[0][1], edge[1][0], edge[1][1], edge[2], edge[3])
      except Exception as e:
          print(f"記錄線段時發生錯誤：{e}")
    
  #找上下公切線
  def FindCommonTangent(self,hull,left_sub_points,right_sub_points):
    
    upperTangent = None
    lowerTangent = None
    
    #建立一個for迴圈跑hull中的每的點以及下一個點，到最後一個點會接回來第一個點
    for i in range(len(hull)):  # 遍歷到倒數第二個點
      current_point = hull[i]
      next_point = hull[(i + 1) % len(hull)]
      # 判斷兩個點是否分別在左子集合和右子集合
      # 判斷兩個點是否分別在左子集合和右子集合
      if current_point in left_sub_points and next_point in right_sub_points:
        lowerTangent = (current_point, next_point)  # 設定上公切線
      elif current_point in right_sub_points and next_point in left_sub_points:
        upperTangent = (current_point, next_point)  # 設定下公切線

    return upperTangent, lowerTangent
    
  #做Hyperplane
  def HyperPlane(self, upperTangent, lowerTangent):
    
    # 當還沒碰到lowerTangent就持續做
    # 流程：碰到,截斷,在重畫   note: upperTangent[0](blue)[右] , upperTangent[1](red)[紅]
    current_Vertex1 = upperTangent[0]  
    current_Vertex2 = upperTangent[1]
    
    # 先做一個暫時性的邊集合交到的點要先刪掉 , note:交到的線intersect_Line , 交到的點intersectX,intersectY
    tmpEdgeSet = self.edges[:]    #創建新列表，寫成tmpEdgeSet = self.edge 同時修改，注意！！！
    hyperPlane_edge = []
    intersect_Line = None 
    intersectX = None 
    intersectY = None
    currentY = 100000000
    checkBreak = 0
    current_bisector = None
    this_bisector = None
    bisector_direction = None
    pre_node = None
    PreLine = None

    # 從 upperTangent 做到 lowerTangent
    while True:
      # 做中垂線(畫和找) ， 先保留在tmpEdgeSet中，並手動畫出圖
      (bisx1,bisy1,bisx2,bisy2) = app.cal_perpendicular_bisector(current_Vertex1[0],current_Vertex1[1],current_Vertex2[0],current_Vertex2[1])
      current_bisector = ((bisx1,bisy1),(bisx2,bisy2))
      
      #定義Pre_node如果None->起始中垂線->就先定為bisector中的高點
      if pre_node==None :
        if bisy1>bisy2:
          pre_node = (bisx1,bisy1)
        else:
          pre_node = (bisx2,bisy2)
          
      # 找到最高的交點y --> for 迴圈
      minDistant = 1000000000
      tmpIntersectX = None
      tmpIntersectY = None
      
      for edge in tmpEdgeSet : 
        (L1,L2,p1,p2) = edge
        Line = (L1,L2,p1,p2)
        intersection = self.FindIntersaction(Line, current_bisector)
        if intersection is None:
          continue
        else:
          tmpIntersectX, tmpIntersectY = intersection
        
          # 比較交點y座標，選擇y值最高的交點
          if tmpIntersectY <= currentY and self.calculate_distance(intersection,pre_node) <= minDistant and PreLine != Line:
            intersectX = tmpIntersectX
            intersectY = tmpIntersectY
            intersect_Line = Line
            minDistant =self.calculate_distance(intersection,pre_node)

      # 找到邊之後 ###################################################################################################################################
      # 下次再做時不考慮這個邊用tmpEdgeSet扣掉 , 並且將prebisector改成此次交點
      if current_Vertex1 not in lowerTangent or current_Vertex2 not in lowerTangent:
        PreLine = intersect_Line
        currentY = intersectY
      else:
        pre_node = (bisx1,bisy1)
        
      # 目前截取到的bisector -> 之後要放進去hyperPlane_edge中
      this_bisector = (pre_node,(intersectX,intersectY),current_Vertex1,current_Vertex2)
      
      # 畫出截斷後的bisector ， 並放進去hyperPlane裡面做紀錄
      app.canvas.create_line(pre_node[0],pre_node[1],intersectX,intersectY,fill="orange")
      stop()
      hyperPlane_edge.append(this_bisector)

      ####################################
      if checkBreak == 1:
        break
      #################################### 終結點 ， 最後一次做完中垂線

      #2. 做交點到保留的那一個線段 (使用外基判斷)：(1)先判斷交到的是左邊的點還是右邊的點 -> 先找到線的parents就能知道左點還是右點了(2)在使用外基CCW function進行截斷操作 
      # note : 需要計算邊的color 之後添加邊的顏色比較好寫 -> red 外基截斷順時針 , blue 外基截斷逆時針 -> 將current_Vertex改下一個點
      color = None 
      # 判斷hyperPlane往下做的下一個點
      (L1,L2,p1,p2) = intersect_Line
      if p1 in self.left_sub_diagram.points:
        color = "red"
        if p1 == current_Vertex2:
          current_Vertex2 = p2
        else:
          current_Vertex2 = p1
      else:
        color = "blue"
        if p1 == current_Vertex1:
          current_Vertex1 = p2
        else:
          current_Vertex1 = p1    
        
      # 令一個intersectPoint表示交點 , 以及bisector direction : (pre_node,interdectPoint)
      intersectPoint = (intersectX,intersectY)
      
      # 如果是同一個點的話，就使用上一次的bisector_direction來做判斷
      if pre_node != (int(intersectX),int(intersectY)):
        bisector_direction = self.VectorFromPoints(pre_node,intersectPoint)
      
      # if color == "red"左 -> (1)刪除那個邊並畫上新的邊(2)把新的邊加入tmpedge中(3)畫出新的邊
      if color == "red":
        #判斷交點跟兩個端點與法向量是順時針還是逆時針（要逆時針的）note: 法向量永遠是取從y大到y小的方向的
        intersection_edge_direction = self.VectorFromPoints(intersectPoint,intersect_Line[0])
        # 如果是左邊的保留逆時針，淘汰順時針方向
        if self.check_direction(bisector_direction,intersection_edge_direction) == "clockwise":
          app.delete_line_by_endpoints(intersect_Line[0][0],intersect_Line[0][1],intersect_Line[1][0],intersect_Line[1][1])
          # 移除舊邊添加新邊 ， 並將PreLine改成正確的值 , 並在畫布上畫上
          tmpEdgeSet.remove(intersect_Line)
          tmpEdgeSet.append((intersectPoint,intersect_Line[0],intersect_Line[2],intersect_Line[3]))
          PreLine = (intersectPoint,intersect_Line[0],intersect_Line[2],intersect_Line[3])
          app.canvas.create_line(intersectX,intersectY,intersect_Line[0][0],intersect_Line[0][1],fill="red")
        else:
          app.delete_line_by_endpoints(intersect_Line[0][0],intersect_Line[0][1],intersect_Line[1][0],intersect_Line[1][1])
          tmpEdgeSet.remove(intersect_Line)
          tmpEdgeSet.append((intersectPoint,intersect_Line[1],intersect_Line[2],intersect_Line[3]))
          PreLine = (intersectPoint,intersect_Line[1],intersect_Line[2],intersect_Line[3])
          app.canvas.create_line(intersectX,intersectY,intersect_Line[1][0],intersect_Line[1][1],fill="red")
          
      # elif color == "blue"右 -> (1)刪除那個邊畫上新的邊(2)把新的邊加入new_edge中(3)畫出新的邊
      if color == "blue":
        #判斷交點跟兩個端點與法向量是順時針還是逆時針（要順時針的）note: 法向量永遠是取從y大到y小的方向的
        intersection_edge_direction = self.VectorFromPoints(intersectPoint,intersect_Line[0])
        # 如果是右邊的保留順時針，淘汰逆時針方向
        if self.check_direction(bisector_direction,intersection_edge_direction) == "counterclockwise":
          app.delete_line_by_endpoints(intersect_Line[0][0],intersect_Line[0][1],intersect_Line[1][0],intersect_Line[1][1])
          tmpEdgeSet.remove(intersect_Line)
          tmpEdgeSet.append((intersectPoint,intersect_Line[0],intersect_Line[2],intersect_Line[3]))
          PreLine = (intersectPoint,intersect_Line[0],intersect_Line[2],intersect_Line[3])
          app.canvas.create_line(intersectX,intersectY,intersect_Line[0][0],intersect_Line[0][1],fill="blue")
        else:
          app.delete_line_by_endpoints(intersect_Line[0][0],intersect_Line[0][1],intersect_Line[1][0],intersect_Line[1][1])
          tmpEdgeSet.remove(intersect_Line)  
          tmpEdgeSet.append((intersectPoint,intersect_Line[1],intersect_Line[2],intersect_Line[3]))
          PreLine =(intersectPoint,intersect_Line[1],intersect_Line[2],intersect_Line[3])
          app.canvas.create_line(intersectX,intersectY,intersect_Line[1][0],intersect_Line[1][1],fill="blue")
      
      ######################################################################
      if current_Vertex1 in lowerTangent and current_Vertex2 in lowerTangent:
        checkBreak = checkBreak + 1
      ###################################################################### 做完後會在做最後一次的bisector話line
      pre_node = intersectPoint
    
    ## 把多餘的邊都刪掉   ######################################################################
    hyperPlane_vertex = []
    #先搜集hyperPlane上所有的邊
    for edge in hyperPlane_edge:
      if edge[0] not in hyperPlane_vertex:
        hyperPlane_vertex.append(edge[0])
      if edge[1] not in hyperPlane_vertex:
        hyperPlane_vertex.append(edge[1])
    
    # 判斷目前所有的邊中有哪些邊不是由hyperPlane延伸出去的(需要跑n/2次因為一邊最多n/2個交點) -> 刪除
    # 創建一個臨時的set叫做tmptmpEdgeSet用來記錄tmpEdgeSet最後正確結果（刪除後的結果）
    tmptmpEdgeSet = []
    for i in range(len(self.points)):
      for edge in tmpEdgeSet:
        if edge[0] in hyperPlane_vertex:
          hyperPlane_vertex.append(edge[1])
          if edge not in tmptmpEdgeSet:
            tmptmpEdgeSet.append(edge)
        if edge[1] in hyperPlane_vertex:
          hyperPlane_vertex.append(edge[0])
          if edge not in tmptmpEdgeSet:
            tmptmpEdgeSet.append(edge)
    
    # 將沒有採計到的那條邊去掉(亦即去掉沒有相連的邊)，並在畫布上去除那條邊
    for edge in tmpEdgeSet:
      if edge not in tmptmpEdgeSet:
        app.delete_line_by_endpoints(edge[0][0],edge[0][1],edge[1][0],edge[1][1])
    
    tmpEdgeSet = tmptmpEdgeSet    
        
    ###################################################################### #################
        
    
    # 完全做完後將結果邊進行合併：tmpEdgeSet + hyperPlane_edge ###################################
    self.edges = tmpEdgeSet + hyperPlane_edge
    app.line_treeview_lexicalorder()
    stop()
    
    ###################################################################### #################
    
  #計算距離
  def calculate_distance(self,point1, point2):
    """
    计算两点之间的欧几里得距离。

    :param point1: 第一个点的坐标，格式为 (x, y) 或 (x, y, z)
    :param point2: 第二个点的坐标，格式为 (x, y) 或 (x, y, z)
    :return: 两点之间的距离
    """
    if len(point1) != len(point2):
        raise ValueError("两点的维度必须相同")
    
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))
    
  #find intersaction
  def FindIntersaction(self, segment1, segment2):
    """
    計算兩條線段的交點
    segment1: [(x1, y1), (x2, y2)] 線段 1 的兩端點
    segment2: [(x3, y3), (x4, y4)] 線段 2 的兩端點
    返回值:
        如果有交點，返回交點坐標 (x, y)
        如果無交點，返回 None
    """
    x1, y1 = segment1[0]
    x2, y2 = segment1[1]
    x3, y3 = segment2[0]
    x4, y4 = segment2[1]

    # 計算線段的向量差
    det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if det == 0:
        # 平行或共線，無交點
        return None

    # 求解交點的參數 t 和 u
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / det
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / det

    # 判斷是否在線段內
    if 0 <= t <= 1 and 0 <= u <= 1:
        # 計算交點坐標
        inter_x = x1 + t * (x2 - x1)
        inter_y = y1 + t * (y2 - y1)
        return (inter_x, inter_y)

    # 交點不在線段範圍內
    return None
  
  def find_closest_points_of_two_sets(self,set1, set2):
    """
    找到集合 set1 和集合 set2 中最近的两点，不返回距离。

    :param set1: 集合 1，列表形式，包含二维点的元组 [(x1, y1), (x2, y2), ...]
    :param set2: 集合 2，列表形式，包含二维点的元组 [(x1, y1), (x2, y2), ...]
    :return: 最近点对 (p1, p2)
    """
    closest_pair = None
    min_distance_squared = float('inf')
    
    # 遍历 set1 和 set2 中所有可能的点对
    for point1 in set1:
        for point2 in set2:
            # 计算距离的平方
            distance_squared = (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2
            if distance_squared < min_distance_squared:
                min_distance_squared = distance_squared
                closest_pair = (point1, point2)

    return closest_pair
      
  def check_direction(self,v1, v2):
    """
    判斷兩個向量之間的方向。
    :param v1: 向量1 (x1, y1)
    :param v2: 向量2 (x2, y2)
    :return: "counterclockwise", "clockwise", or "collinear"
    """
    x1, y1 = v1
    x2, y2 = v2
    
    cross = x1 * y2 - y1 * x2
    
    if cross > 0:
      return "counterclockwise"  # 逆時針
    elif cross < 0:
      return "clockwise"  # 順時針
    else:
      return "collinear"  # 共線
  
  #找ConvexHull
  def ConvexHull(self):
    
    hull = []
    startPoint = self.getMinYPoint()  # 起始點是 y 最小的點
    hull.append(startPoint)
    prevertex = startPoint  # 上一個點，初始化為起始點

    while True:
      candidate = None
      for point in self.points:
        if point == prevertex: 
          continue  # 跳過上一個選中的點

        if candidate is None:
          candidate = point  # 初始候選點
          continue

        ccw_value = self.CheckCCW(prevertex, candidate, point)
        if ccw_value == 0 and self.pointDist(prevertex, candidate) > self.pointDist(prevertex, point):
          vector1 = self.VectorFromPoints(prevertex,candidate)
          vector2 = self.VectorFromPoints(prevertex,point)
          if self.CheckVectorDirection(vector1,vector2) == 0: 
            continue
          candidate = point  # 共線時，選擇距離最近的點
          
        elif ccw_value < 0:
          candidate = point  # 順針時，更新候選點

      if candidate == startPoint:
        break  # 回到起點，終止迴圈
      hull.append(candidate)
      prevertex = candidate  # 更新上一個選中的點
    
    return hull

  def draw_hull(self,hull):
    if len(hull) < 2:
        return
    
    # 繪製點之間的連線
    for i in range(len(hull)):
        x1, y1 = hull[i]
        x2, y2 = hull[(i + 1) % len(hull)]  # 與下一點連接，最後一點連回第一點
        app.canvas.create_line(x1, y1, x2, y2, fill="purple", width=2)


############# 找convex hull 用到的 function  ############# ########### ########### 
  
  def getMinYPoint(self):
    # 找到 y 最小的點，若 y 相同則返回 x 最小的點
    return min(self.points, key=lambda p: (p[1], p[0]))
  
  #同一條線不能往回找判斷:Dot
  def CheckVectorDirection(self,u, v):
    """
    判斷兩個向量是否同向或反向
    u, v: 向量，格式為 (dx, dy)
    返回值：
        1 表示同方向
        0 表示反方向
    """
    # 防止零向量的特殊情況
    if u == (0, 0) or v == (0, 0):
        raise ValueError("無法判斷零向量的方向")

    # 計算比例
    ratio_x = v[0] / u[0] if u[0] != 0 else None
    ratio_y = v[1] / u[1] if u[1] != 0 else None

    # 判斷是否為同方向或反方向
    if ratio_x is not None and ratio_y is not None and ratio_x == ratio_y:
        return 1 if ratio_x > 0 else 0
    elif ratio_x is None and ratio_y is not None:  # u[0] 為 0，但 v[0] 也應該是 0
        return 1 if v[1] / u[1] > 0 else 0
    elif ratio_y is None and ratio_x is not None:  # u[1] 為 0，但 v[1] 也應該是 0
        return 1 if v[0] / u[0] > 0 else 0

    # 其他情況：非同方向或反方向
    return 0
  
  def VectorFromPoints(self, A, B):
    """
    計算從點 A 到點 B 的向量
    A, B: 二維座標點，格式為 (x, y)
    返回向量 (dx, dy)
    """
    return (B[0] - A[0], B[1] - A[1])
    
  #找ConvexHull
  def CheckCCW(self, p, q, r):
    """計算 p, q, r 三點的叉積，用來判斷是否逆時針 (ccw > 0)、順時針 (ccw < 0) 或共線 (ccw == 0)"""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

  def pointDist(self, p1, p2):
    """計算兩點 p1 和 p2 之間的歐幾里得距離"""
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
  
  def is_collinear(self):
    # 如果少於3個點，直接返回 True，因為兩個點必定共線
    if len(self.points) < 3:
      return True

    # 取第一個點和第二個點作為基準
    p1 = self.points[0]
    p2 = self.points[1]

    # 檢查所有後續的點是否與前兩個點共線
    for i in range(2, len(self.points)):
      p3 = self.points[i]
      # 計算叉積來判斷三點是否共線
      cross_product = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
      
      if cross_product != 0:  # 叉積不為零，代表三個點不共線
        return False

    # 如果沒有發現不共線的點，返回 True
    return True

########### ########### ########### ########### ########### ########### ########### 

############# 設計lock 用到的 class  ############# ########### ########### def stop():
    
running = False
paused = True
    
def stop():
  global paused
  while paused:
      root.update()  # 不斷刷新 Tkinter 界面，保持 GUI 響應
  if(running):return
  paused = True  # 重置 paused 狀態，等待下一次暫停

def next_step():
  global paused
  paused = False

def run():
  global running
  global paused
  paused=False
  running=True
    
root = tk.Tk()
app = VoronoiDiagram(root)
root.mainloop()
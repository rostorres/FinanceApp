from flask import Flask, render_template, json, request, session, redirect, url_for
from flaskext.mysql import MySQL
import pygal

mysql = MySQL()
app = Flask(__name__)
app.secret_key = '123456'

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'Financiera'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

with open('./static/json/taza_anual.json') as json_file_anual:
    i_anual_dict = json.load(json_file_anual)

# taza de interés anual cobrada al cliente
intereses = i_anual_dict['taza'] / 12

with open('./static/json/intereses.json') as json_file_mensual:
    i_mensual = json.load(json_file_mensual)

# taza de rendiimento mensual de los fondos
i_fija = list(i_mensual['fija'].values())
i_var = list(i_mensual['var'].values())
i_mod = list(i_mensual['mod'].values())
i_alto = list(i_mensual['alto'].values())

with open('./static/json/mes_vencido.json') as json_file_mes_vencido:
    mes_vencido_dict = json.load(json_file_mes_vencido)

# mes vencido que será enseñado en el gráfico
mes_venc = mes_vencido_dict['mes_vencido']

# mes vencido que será enseñado en el gráfico
anno = mes_vencido_dict['anno']

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/verRegistro')
def verRegistro():
    return render_template('registro.html')

@app.route('/verLogin')
def verLogin():
    return render_template('login.html')

@app.route('/registro',methods=['POST'])
def registro():
    try:
        _nombreInput = request.form['nombre']
        _emailInput = request.form['email']
        _passInput = request.form['clave']

        if _nombreInput and _emailInput and _passInput:
            
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('crearUsuario',(_nombreInput,_emailInput,_passInput))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'Usuario creado con exito!'})
            else:
                return json.dumps({'error':str(data[0])})  
        else:
            return json.dumps({'html':'<span>Introduzca los campos necesarios.</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/validarLogin',methods=['POST'])
def validarLogin():
    try:
        _emailForm = request.form['email']
        _passForm = request.form['clave'] 
 
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('validarLogin',(_emailForm,))
        data = cursor.fetchall()
 
        if len(data) > 0:
            if str(data[0][3]) ==  _passForm:
                session['user'] = data[0][0]
                return redirect('/principal')
            else:
                return render_template('error.html',error = 'Correo o clave incorrectos.')
        else:
            return render_template('error.html',error = 'Correo o clave incorrectos.') 
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/principal')
def principal():
    if session.get('user'):
        return render_template('principal.html')
    else:
        return render_template('error.html',error = 'Acceso no autorizado.')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/verSimular')
def verSimular():
    return render_template('simular.html')

@app.route('/simular',methods=['POST'])
def simular():
    if "btnSolicitar" in request.form:
        try:
            if session.get('user'):
                try:        
                    _imputValor = float(request.form['inputValor'])
                    _inputMeses = int(request.form['inputMeses'])

                    # validate the received values
                    if _imputValor and _inputMeses:
                        _user = session.get('user')
    
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.callproc('addSolicitud',(_imputValor,_inputMeses,_user))
                        data = cursor.fetchall()
            
                        if len(data) is 0:
                            conn.commit()
                            return redirect('principal')
                        else:
                            return render_template('error.html',error = 'An error occurred!')
                    else:
                        return json.dumps({'html':'<span>Introduzca los campos necesarios.</span>'})

                except Exception as e:
                    return render_template('error.html',error = str(e))

            else:
                return render_template('error.html',error = 'Unauthorized Access')

        except Exception as e:
            return render_template('error.html',error = str(e))

        finally:
            cursor.close()
            conn.close()
    else:        
        try:        
            _imputValor = float(request.form['inputValor'])
            _inputMeses = int(request.form['inputMeses'])

            # validate the received values
            if _imputValor and _inputMeses:

                # calculo de la mensualidad: P (((1 + i)^n)*i) / (((1+i)^n)-1)      
                _mensualidad = round(_imputValor * (((1 + (intereses/12) ) ** _inputMeses) * (intereses/12)) / (((1 + (intereses/12)) ** _inputMeses) -1), 2)            
    
                return render_template('simular.html', resTexto = 'Resultado = ' , resValor = _imputValor, resMeses = _inputMeses, resMensualidad = _mensualidad)

            else:
                return json.dumps({'html':'<span>Introduzca los campos necesarios.</span>'})

        except Exception as e:
            return render_template('error.html',error = str(e))

@app.route('/buscarFinanc')
def buscarFinanc():
    try:
        if session.get('user'):
            _user = session.get('user')
 
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('getFin',(_user,))
            financs = cursor.fetchall()
 
            financs_dict = []
            for fin in financs:
                financ_dict = {
                        'Id': fin[0],
                        'Total': fin[1],
                        'meses': fin[2],
                        'Mensualidad': fin[3],
                        'mesActual': fin[5],
                        'mesesRetraso': fin[7],
                        'ImporteRetraso': fin[8]}
                financs_dict.append(financ_dict)

            return json.dumps(financs_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access - error 4')
    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/verInversiones')
def verInversiones():
    try:
        if session.get('user'):
            _user = session.get('user')
 
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('getInver',(_user,))
            invers = cursor.fetchall()
 
            invers_array = []
            inver_array = []
            renta_fija = []
            renta_var = []
            renta_mod = []
            renta_alto = []
            _r_fija_value = None
            _r_var_value = None
            _r_mod_value = None
            _r_alto_value = None

            for inver in invers:
                inver_list = list(inver)
                inver_array = []
                _producto = inver_list[1]
                _valor = inver_list[2]
                inver_array.append(_producto)
                inver_array.append(_valor)
                invers_array.append(inver_array)
            
            for inv in invers_array:
                if inv[0] == 1:
                    _r_fija_value = inv[1]
                elif inv[0] == 2:
                    _r_var_value = inv[1]
                elif inv[0] == 3:
                    _r_mod_value = inv[1]
                elif inv[0] == 4:
                    _r_alto_value = inv[1]

            for i in range(0, mes_venc):
                if _r_fija_value:
                    _v_fija_corrig = _r_fija_value * (1 + i_fija[i])
                    renta_fija.append(_v_fija_corrig)
                if _r_var_value:
                    _v_var_corrig = _r_var_value * (1 + i_var[i])
                    renta_var.append(_v_var_corrig)
                if _r_mod_value:
                    _v_mod_corrig = _r_mod_value * (1 + i_mod[i])
                    renta_mod.append(_v_mod_corrig)
                if _r_alto_value:
                    _v_alto_corrig = _r_alto_value * (1 + i_alto[i])
                    renta_alto.append(_v_alto_corrig)

            try:
                graph = pygal.Line(interpolate='cubic')
                graph.title = 'Rendimiento Inversiones año ' + str(anno)
                graph.x_labels = ['ene','feb','mar','abr','may','jun','jul','ago','sept','oct','nov','dic']

                if len(renta_fija) > 0 :
                    graph.add('Renta Fija', renta_fija)
                if len(renta_var) > 0 :
                    graph.add('Renta Variable', renta_var)
                if len(renta_mod) > 0 :
                    graph.add('Riesgo Moderado', renta_mod)
                if len(renta_alto) > 0 :
                    graph.add('Alto Riesgo', renta_alto)
                
                graph_data = graph.render_data_uri()

                return render_template("inversiones.html", graph_data = graph_data)

            except Exception as e:
                return render_template('error.html', error = str(e)) 
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        cursor.close()
        con.close()

if __name__ == "__main__":
    app.run()

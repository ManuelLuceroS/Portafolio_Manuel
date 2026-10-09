import { useEffect } from "react";
import { Link } from "react-router-dom";
import { Download, Linkedin, Mail } from "lucide-react";
import ProjectCard from "../components/ProjectCard";
import {
  contacto,
  educacion,
  enfoques,
  enlaceActivo,
  experiencia,
  habilidades,
  indicadores,
  laboratorio,
  perfil,
  proyectos,
} from "../data/portfolio";

export default function Home() {
  useEffect(() => {
    document.title = "Manuel Lucero | Analista de Datos y Desarrollador";
  }, []);

  const github = enlaceActivo(contacto.github);
  const linkedin = enlaceActivo(contacto.linkedin);

  return (
    <main id="contenido">
      <section id="inicio" className="hero">
        <div className="contenedor">
          <p className="ubicacion">{perfil.ubicacion}</p>
          <p className="nombre-hero">{perfil.nombre}</p>
          <h1>{perfil.saludo}</h1>
          <p className="titulo-hero">{perfil.tituloCorto}</p>
          <p className="titulo-largo">{perfil.titulo}</p>
          <div className="descripcion">
            {perfil.descripcion.map((parrafo) => (
              <p key={parrafo}>{parrafo}</p>
            ))}
          </div>
          <div className="acciones">
            <Link className="boton boton-primario" to="/#proyectos">
              Ver proyectos
            </Link>
            <a className="boton boton-secundario" href={perfil.cv} download>
              <Download size={16} aria-hidden="true" />
              Descargar CV
            </a>
            <Link className="boton boton-secundario" to="/#contacto">
              Contactarme
            </Link>
          </div>
          <div className="redes redes-hero">
            {linkedin ? (
              <a href={contacto.linkedin.trim()} target="_blank" rel="noopener noreferrer">
                <Linkedin size={16} aria-hidden="true" />
                LinkedIn
              </a>
            ) : null}
            {github ? (
              <a href={contacto.github.trim()} target="_blank" rel="noopener noreferrer">
                GitHub
              </a>
            ) : null}
          </div>
          <ul className="indicadores">
            {indicadores.map((item) => (
              <li key={item.valor}>
                <strong>{item.valor}</strong>
                {item.detalle ? <span>{item.detalle}</span> : null}
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section id="sobre-mi" className="seccion seccion-alt">
        <div className="contenedor sobre-mi">
          <h2>Sobre mí</h2>
          <p>
            Soy Tecnólogo en Análisis y Desarrollo de Software del SENA y estudiante de Ingeniería
            de Sistemas en la Universidad Nacional Abierta y a Distancia (UNAD), actualmente en
            quinto semestre.
          </p>
          <p>
            Cuento con experiencia en <strong>análisis de datos</strong>,{" "}
            <strong>Business Intelligence</strong>, <strong>automatización</strong> de procesos y{" "}
            <strong>desarrollo de software</strong>.
          </p>
          <p>
            He trabajado en la creación y mantenimiento de más de 20 reportes empresariales,
            integrando información desde <strong>bases de datos</strong> SQL y transformándola en
            indicadores y dashboards.
          </p>
          <p>
            También he desarrollado aplicaciones utilizando Python, Django, Flutter y APIs REST.
          </p>
          <p>
            Me interesa construir soluciones tecnológicas que faciliten el acceso a la información,
            reduzcan tareas manuales y mejoren la gestión de los procesos empresariales.
          </p>
          <ul className="enfoques">
            {enfoques.map((enfoque) => (
              <li key={enfoque}>{enfoque}</li>
            ))}
          </ul>
        </div>
      </section>

      <section id="experiencia" className="seccion">
        <div className="contenedor">
          <h2>Experiencia</h2>
          <div className="linea-tiempo">
            {experiencia.map((item) => (
              <article className="experiencia" key={`${item.empresa}-${item.periodo}`}>
                <div className="experiencia-encabezado">
                  <div>
                    <h3>{item.cargo}</h3>
                    <p className="empresa">
                      {item.empresa}
                      {item.proyecto ? ` · ${item.proyecto}` : ""}
                    </p>
                  </div>
                  <p className="periodo">{item.periodo}</p>
                </div>
                <p className="lugar">{item.lugar}</p>
                <p>{item.descripcion}</p>
                <ul className="actividades">
                  {item.logros.map((logro) => (
                    <li key={logro}>{logro}</li>
                  ))}
                </ul>
                {item.tecnologias ? (
                  <ul className="tecnologias tecnologias-experiencia">
                    {item.tecnologias.map((tecnologia) => (
                      <li key={tecnologia}>{tecnologia}</li>
                    ))}
                  </ul>
                ) : null}
                {item.enlace ? (
                  <a
                    className="boton boton-texto"
                    href={item.enlace.href}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {item.enlace.texto}
                  </a>
                ) : null}
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="proyectos" className="seccion seccion-alt">
        <div className="contenedor">
          <h2>Proyectos</h2>
          <p className="intro-seccion">
            Trabajos de análisis, automatización y desarrollo. No publico tableros ni datos de las
            empresas.
          </p>
          <div className="rejilla-proyectos">
            {proyectos.map((proyecto) => (
              <ProjectCard key={proyecto.id} proyecto={proyecto} />
            ))}
          </div>

          <h3 className="subtitulo-seccion" id="laboratorio">
            Laboratorio de análisis de datos
          </h3>
          <p className="intro-seccion">
            Estos tres ejercicios usan datos ficticios. Las cifras de cada dashboard salen del
            análisis en Python y no corresponden a una empresa real.
          </p>
          <div className="rejilla-proyectos">
            {laboratorio.map((proyecto) => (
              <ProjectCard key={proyecto.id} proyecto={proyecto} />
            ))}
          </div>
        </div>
      </section>

      <section id="habilidades" className="seccion">
        <div className="contenedor">
          <h2>Habilidades</h2>
          <div className="rejilla-habilidades">
            {habilidades.map((grupo) => (
              <article className="tarjeta" key={grupo.grupo}>
                <h3>{grupo.grupo}</h3>
                <ul className="lista-habilidades">
                  {grupo.items.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="educacion" className="seccion seccion-alt">
        <div className="contenedor">
          <h2>Educación</h2>
          <div className="rejilla-educacion">
            {educacion.map((estudio) => (
              <article className={estudio.enCurso ? "tarjeta tarjeta-curso" : "tarjeta"} key={estudio.titulo}>
                {estudio.enCurso ? <p className="etiqueta-curso">En curso</p> : null}
                <h3>{estudio.titulo}</h3>
                <p>{estudio.institucion}</p>
                <p className="periodo">{estudio.periodo}</p>
                {estudio.detalle ? <p className="detalle-estudio">{estudio.detalle}</p> : null}
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="contacto" className="seccion">
        <div className="contenedor estrecho">
          <h2>Contacto</h2>
          <p>
            Si buscas apoyo en análisis de datos o desarrollo de software, puedes escribirme.
          </p>
          <p className="lugar">{perfil.ubicacion}</p>
          <div className="acciones">
            <a className="boton boton-primario" href={`mailto:${contacto.correo}`}>
              <Mail size={16} aria-hidden="true" />
              Enviar correo
            </a>
            {linkedin ? (
              <a
                className="boton boton-secundario"
                href={contacto.linkedin.trim()}
                target="_blank"
                rel="noopener noreferrer"
              >
                <Linkedin size={16} aria-hidden="true" />
                LinkedIn
              </a>
            ) : null}
            {github ? (
              <a
                className="boton boton-secundario"
                href={contacto.github.trim()}
                target="_blank"
                rel="noopener noreferrer"
              >
                GitHub
              </a>
            ) : null}
            <a className="boton boton-secundario" href={perfil.cv} download>
              <Download size={16} aria-hidden="true" />
              Descargar CV
            </a>
          </div>
          <p>
            <a href={`mailto:${contacto.correo}`}>{contacto.correo}</a>
          </p>
          {github ? null : (
            <p className="nota">
              El enlace de GitHub se configura en <code>src/data/portfolio.js</code>.
            </p>
          )}
        </div>
      </section>
    </main>
  );
}

package coop.rchain.shared

import cats.tagless._

sealed trait Event
object Event {
  final case class NodeStarted(address: String)                             extends Event
  final case class EnteredRunningState(blockHash: String)                   extends Event
  final case class ApprovedBlockReceived(blockHash: String)                 extends Event
  final case class SentUnapprovedBlock(blockHash: String)                   extends Event
  final case class BlockApprovalReceived(blockHash: String, sender: String) extends Event
  final case class SentApprovedBlock(blockHash: String)                     extends Event
}

@autoFunctorK
@autoSemigroupalK
@autoProductNK
trait EventLog[F[_]] {
  def publish(event: Event): F[Unit]
}

object EventLog {
  def apply[F[_]](implicit E: EventLog[F]): EventLog[F] = E

  implicit val EventLoggerLogSource: LogSource = LogSource(classOf[EventLogger])

  def eventLogger[F[_]: Log]: EventLog[F] =
    (event: Event) => Log[F].info(event.getClass.getSimpleName.stripSuffix("$"))
}

class EventLogger() // Dummy class for the logger name
